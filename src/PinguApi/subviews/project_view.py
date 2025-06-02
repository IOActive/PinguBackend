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

import logging
import yaml
from PinguApi.submodels.project import Project
from PinguApi.serializers.project_serializer import ProjectSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import APIException, NotAcceptable

from src.PinguApi.utilities.configuration import replace_test_prefix, get_all_buckets
from PinguApi.tasks import create_project_buckets, delete_project_buckets

logger = logging.getLogger(__name__)

class Project_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']
    
    serializer_class = ProjectSerializer
    
    queryset = Project.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        try:
            project_name = request.data.get('name')
        
        except Exception as e:
            raise NotAcceptable(detail="The project name is mandatory")
        
        try:
            with open("default_yml_configs/deafult_project_config.yaml", "r") as f:
                default_config = yaml.safe_load(f.read())
            
            config = replace_test_prefix(data=default_config, new_prefix=f"{project_name}-")
            
            request.data['configuration'] = yaml.safe_dump(config)
        except Exception as e:
            raise APIException(detail="Failed to generate default project config")
        
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer: ProjectSerializer):
        """Ensure task is executed after successful save."""
        project = serializer.save()  # Save to DB first
        self.post_save_task(project)  # Execute task after saving

    def post_save_task(self, project: Project):
        """Task to execute after saving."""
        # Replace with your desired task logic (e.g., logging, external API call)
        configuration_y = yaml.safe_load(project.configuration)
        buckets = get_all_buckets(configuration_y)
        success = create_project_buckets.apply(args=[buckets]).get()
        if success:
            logger.info("Project succesfully created")
        else:
            logger.error("Failed to create project buckets")
            project.delete()
            raise APIException(detail="Failed to create project buckets", code=500)


class Project_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
    def perform_destroy(self, instance: Project):
        """Ensure task is executed after successful save."""
        self.post_delete_task(instance)  # Execute task after saving
        instance.delete()


    def post_delete_task(self, project: Project):
        """Task to execute after saving."""
        # Replace with your desired task logic (e.g., logging, external API call)
        configuration_y = yaml.safe_load(project.configuration)
        buckets = get_all_buckets(configuration_y)
        success = delete_project_buckets.apply(args=[buckets]).get()
        if success:
            logger.info("Project succesfully delete")
        else:
            logger.error("Failed to delete project buckets")
            raise APIException(detail="Failed to delete project buckets", code=500)


