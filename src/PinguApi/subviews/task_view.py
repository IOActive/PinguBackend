# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
from datetime import datetime
import json
from django.http import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.handlers.work_queue import publish, get_queue_element, queue_exists, read_queue_elements
from PinguApi.submodels.job import Job
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.submodels.platforms import Supported_Platforms
from PinguApi.submodels.task import Task
from PinguApi.serializers.task_serializer import TaskSerializer
from rest_framework import generics
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin
from PinguApi.tasks import download_task_logs
from django.core.exceptions import ObjectDoesNotExist
from PinguApi.submodels.project import Project
from src.PinguApi.utilities import configuration
import yaml

from rest_framework.exceptions import NotAcceptable, ValidationError, NotFound, APIException

class Task_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class Task_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'job', 'command', 'platform', 'job__project']
    queryset = Task.objects.all().order_by('-create_time')
    serializer_class = TaskSerializer
    
    def get_task_from_queue(self, platform):
        queue = 'jobs-%s' % platform
        empty, task = get_queue_element(queue.lower())
        if not empty:
            response = Response(task)
            response.status_code = 200
            return response
        else:
            raise NotFound(detail='empty queue', code=404)
        
    def get(self, request, *args, **kwargs):
        data = request.query_params
        if 'read_queue' in data:
            json_object = json.loads("{\"results\": []}")
            empty = True
            for platform in Supported_Platforms:
                queue = f'jobs-{platform.value}'
                empty, tasks = read_queue_elements(queue)
                if not empty:
                    json_object['results'] = tasks
                
            if len(json_object['results']) > 0:
                response = Response(json_object)
                response.status_code = 200
                return response
            else:
                raise NotFound(detail='queue does not exist', code=404)
        
        elif 'platform' in data:
            platform = data['platform']
            queue_response = self.get_task_from_queue(platform)
            if queue_response.status_code == 200:
                return queue_response
            else:
                raise NotFound(detail='queue does not exist', code=404)
        
        else:
            try:
                tasks = self.filter_queryset(self.get_queryset())
                tasks_page = self.paginate_queryset(tasks)
                
                for task in tasks_page:
                    project = Project.objects.get(id=task.job.project.id)
                    bucket_name = configuration.get_value(yaml.safe_load(project.configuration), "logs.bot.bucket")
                    bucket_path = f"{task.job.name}/{task.id}/"
                    logs = download_task_logs.apply(args=[bucket_name, bucket_path]).get()
                    if logs['bot_log']:
                        task.bot_log = base64.b64encode(logs['bot_log']).decode('utf-8')
                    if logs['heartbeat_log']:
                        task.heartbeat_log = base64.b64encode(logs['heartbeat_log']).decode('utf-8')
                    if logs['run_fuzzer_log']:
                        task.run_fuzzer_log = base64.b64encode(logs['run_fuzzer_log']).decode('utf-8')
                    if logs['run_heartbeat_log']:
                        task.run_heartbeat_log = base64.b64encode(logs['run_heartbeat_log']).decode('utf-8')
                serializer = TaskSerializer(tasks_page, many=True)
                return self.get_paginated_response(serializer.data)
            except ObjectDoesNotExist as e:
                return JsonResponse({"results": []}, safe=False)
            except Exception as e:
                raise APIException(detail="Faild to get the task details")
                
    def post(self, request, *args, **kwargs):
        body = request.data
        command = body.get('command')
        argument = body.get('argument')
        platform = body.get('platform')
        job_id = body.get('job_id')

        if job_id is None:
            raise ValidationError(detail="Job ID is required", code=400)

        try:
            job_id = Job.objects.get(id=job_id)
        except Exception as e:
            raise NotFound(detail='Job ID is invalid', code=404)

        if (command is None) or (argument is None):
            raise NotAcceptable(detail='missing command or argument parameters', code=400)

        if job_id.platform != platform:
            raise NotAcceptable(detail='Tasks platform does not match the Job platform', code=406)

        queue = 'jobs-%s' % job_id.platform
        # lowercase queue
        queue = queue.lower()
        if not queue_exists(queue):
            raise NotFound(detail="Queue does not exists", code=404)
        

        
        task = Task(job=job_id, 
                    command=command, 
                    argument=argument, 
                    platform=platform,
                    payload="",
                    create_time=datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        )

        queue_task = {
            'task_id': str(task.id),
            'job_id': str(job_id.id),
            'platform': platform,
            'command': command,
            'argument': argument,
        }

        publish(queue, json.dumps(queue_task))

        task.save()

        response = Response({'success': True, 'detail': 'Tasks Published'})
        response.status_code = 201
        return response