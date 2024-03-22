from django.shortcuts import render
import json
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.utils.workQueue import create_queue, publish, get_queue_element, queue_exists, read_queue_elements
from PinguApi.submodels.Job import Job
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.submodels.Platforms import Supported_Platforms



class Task_APIView(APIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
    def get(self, request):
        data = request.query_params
        if 'platform' not in data:
            json_object = json.loads("{\"results\": {}}")
            empty = True
            for platform in Supported_Platforms:
                queue = f'tasks-{platform.value}'
                empty, tasks = read_queue_elements(queue)
                if not empty:
                    json_object['results'] = tasks
                
            if len(json_object['results']) > 0:
                response = Response(json_object)
                response.status_code = 200
                return response
            else:
                response = Response({'success': False, 'msg': 'empty queue'})
                response.status_code = 404
                return response
        
        if 'platform' in data:
            platform = data['platform']
            queue = 'tasks-%s' % platform
            empty, task = get_queue_element(queue)
            if not empty:
                response = Response(task)
                response.status_code = 200
                return response
            else:
                response = Response({'success': False, 'msg': 'empty queue'})
                response.status_code = 404
                return response
        else:
            response = Response({'success': False, 'msg': 'queue does not exist'})

            response.status_code = 404
            return response
            
    def post(self, request):
        body = request.data
        command = body.get('command')
        argument = body.get('argument')
        platform = body.get('platform')
        job_id = body.get('job_id')

        if job_id is None:
            response = Response({'success': False, 'msg': 'Job ID not specified'})
            response.status_code = 400
            return response

        job = Job.objects.get(id=job_id)

        if (command is None) or (argument is None):
            response = Response({'success': False, 'msg': 'missing command or argument parameters'})
            response.status_code = 400
            return response

        if job.platform != platform:
            response = Response({'success': False, 'msg': 'Tasks platform does not math the Job platform'})
            response.status_code = 406
            return response

        queue = 'tasks-%s' % job.platform
        if not queue_exists(queue):
            create_queue(queue)

        task = {'job_id': str(job.id),
                'platform': platform,
                'command': command,
                'argument': argument,
                }
        publish( queue, json.dumps(task))
        response = Response({'success': True, 'msg': 'Tasks Published'})
        response.status_code = 201
        return response