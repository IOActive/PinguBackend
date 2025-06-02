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

import os
from django.http import FileResponse
from PinguApi.submodels.build import Build, Supported_Builds
from PinguApi.serializers.build_serializer import BuildSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from src.PinguApi.subviews.storage.build_view import APIView
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.tasks import upload_build_to_bucket, download_build_from_bucket, remove_build_from_bucket, get_build_from_cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, NotAcceptable
from src.PinguApi.utilities import configuration

import base64
import yaml

from PinguApi.submodels.project import Project
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import APIException, NotAcceptable, NotFound

class BuildDownloadView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        build_id = kwargs.get('pk')

        try:
            build = Build.objects.get(id=build_id)
        except ObjectDoesNotExist as e:
            raise NotFound(detail="Build not found", code=404)
        
        try:
            project = Project.objects.get(id=build.project.id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)

        try:
            bucket_name = configuration.get_value(key_path=f"build.{build.type.lower()}.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)

        try:
            build_stream = get_build_from_cache.apply(args=[bucket_name, build.filename]).get()
            
            # Ensure full file is available
            build_stream.seek(0, os.SEEK_END)
            file_size = build_stream.tell()
            build_stream.seek(0)
            
        except Exception as e:
            raise APIException("Failed to download build", code=500)

        response = FileResponse(build_stream, content_type="application/zip")
        response["Content-Length"] = file_size
        response["Content-Disposition"] = f'attachment; filename="{build.filename}.zip"'
        return response


class Build_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'filename', 'type', 'project']
    
    queryset = Build.objects.all()

    serializer_class = BuildSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads

    
    def get(self, request, *args, **kwargs):
        try:
            builds = self.filter_queryset(self.get_queryset())
            builds_page = self.paginate_queryset(builds)
            for build in builds_page:
                download_build_from_bucket.delay(build.blobstore_path)
            serializer = BuildSerializer(builds_page, many=True)
            return self.get_paginated_response(serializer.data)
        except ObjectDoesNotExist as e:
            raise NotFound(detail="Build not found", code=404)
            
    def post(self, request, *args, **kwargs):
        zip_file = request.FILES.get('build_zip')
        zip_file_name = request.data['filename']
        build_type = request.data['type']
        try:
            project = Project.objects.get(id=request.data['project_id'])
        except ObjectDoesNotExist as e:
            raise NotFound(detail="Project not found", code=404)
                
        bucket_name = configuration.get_build_bucket_by_type(build_type=build_type, configuration=yaml.safe_load(project.configuration))
        
        try:
            file =  {
                    "name": zip_file.name,
                    "content": base64.b64encode(zip_file.read()).decode('utf-8'),  # Encode bytes as base64 string
                    "content_type": zip_file.content_type
            }
            upload_build_to_bucket.delay(file, bucket_name)
            
        except Exception as e:
            raise APIException("Failed to get bucket name from configuration", code=500)
        
        request.data['blobstore_path'] =  f"{bucket_name}/{zip_file_name}"
        request.data['file_size'] = zip_file.size
        return self.create(request, *args, **kwargs)


class Build_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads

    
    def delete(self, request, *args, **kwargs):
        remove_build_from_bucket.apply(args=[self.get_object().blobstore_path]).get()
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.FILES.get('build_zip'):
            zip_file = request.FILES.get('build_zip')
            zip_file_name = request.data['filename']
            
            try:
                project = Project.objects.get(id=request.data['project_id'])
            except ObjectDoesNotExist as e:
                raise NotFound(detail="Project not found", code=404)
            
            build_id = kwargs.get('pk')
            if not build_id:
                raise NotAcceptable(detail="Build ID not provided")
            
            try:
                build_type = Build.objects.get(id=build_id).type
            except ObjectDoesNotExist as e:
                raise NotFound(detail="Build not found", code=404)
            
            bucket_name = configuration.get_build_bucket_by_type(build_type=build_type, configuration=yaml.safe_load(project.configuration))
            
            if not bucket_name:
                raise NotFound(detail="Build Bucket not found", code=404)
            try:
                file =  {
                    "name": zip_file.name,
                    "content": base64.b64encode(zip_file.read()).decode('utf-8'),  # Encode bytes as base64 string
                    "content_type": zip_file.content_type
                }
                
                upload_build_to_bucket.delay(file, bucket_name)
            except Exception as e:
                raise APIException("Failed to get bucket name from configuration", code=500)
            
            request.data['blobstore_path'] = f"{bucket_name}/{zip_file_name}"
            request.data['file_size'] = zip_file.size
        else:
            raise NotAcceptable(detail="Build ZIP file not provided")
        return self.update(request, *args, **kwargs)


