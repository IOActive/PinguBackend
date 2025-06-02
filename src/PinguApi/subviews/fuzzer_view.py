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
import os
from django.http import FileResponse, StreamingHttpResponse
import yaml
import base64

from PinguApi.submodels.fuzzer import Fuzzer
from PinguApi.serializers.fuzzer_serializer import FuzzerSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.tasks import upload_fuzzer_to_bucket, download_fuzzer_from_bucket, remove_fuzzer_from_bucket, get_fuzzer_from_cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, APIException, NotAcceptable
from PinguApi.utilities import configuration
from PinguApi.submodels.project import Project
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class Fuzzer_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'builtin', 'project']
    
    queryset = Fuzzer.objects.all()

    serializer_class = FuzzerSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads

    
    def get(self, request, *args, **kwargs):
        try:
            fuzzers = self.filter_queryset(self.get_queryset())
            fuzzers_page = self.paginate_queryset(fuzzers)
            for fuzzer in fuzzers_page:
                if not fuzzer.builtin:
                    download_fuzzer_from_bucket.apply(args=[fuzzer.blobstore_path]).get()

            serializer = FuzzerSerializer(fuzzers_page, many=True)
            return self.get_paginated_response(serializer.data)
        except ObjectDoesNotExist as e:
            raise NotFound(detail="Fuzzer not found", code=404)
        except Exception as e:
            raise APIException(detail="An error occurred while retrieving fuzzers", code=500)
            
    def post(self, request, *args, **kwargs):
        try:
            zip_file = request.FILES.get('fuzzer_zip')
            zip_file_name = request.data['name']
            project_id = request.data['project_id']
            
            if not zip_file or not zip_file_name or not project_id:
                raise NotAcceptable(detail="Missing required fields", code=400)
            try:
                project = Project.objects.get(id=project_id)
            except ObjectDoesNotExist:
                raise NotFound(detail=f"Project with id {project_id} does not exist", code=404)
            try:
                bucket_name = configuration.get_value(key_path="fuzzers.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)
            
            try:
                file =  {
                    "name": zip_file.name,
                    "content": base64.b64encode(zip_file.read()).decode('utf-8'),  # Encode bytes as base64 string
                    "content_type": zip_file.content_type
                }
                upload_fuzzer_to_bucket.delay(file, bucket_name)
            except Exception as e:
                raise APIException(f"Failed to upload fuzzer to bucket", code=500)
            
            request.data['blobstore_path'] = f"{bucket_name}/{zip_file_name}"
            request.data['file_size'] = zip_file.size
            
            return self.create(request, *args, **kwargs)
        except Exception as e:
            raise APIException(detail="An error occurred while uploading the fuzzer", code=500)


class Fuzzer_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Fuzzer.objects.all()
    serializer_class = FuzzerSerializer
    
    def delete(self, request, *args, **kwargs):
        try:
            remove_fuzzer_from_bucket.apply(args=[self.get_object().blobstore_path]).get()
            return self.destroy(request, *args, **kwargs)
        except Exception as e:
            raise APIException(detail="An error occurred while deleting the fuzzer", code=500)

    def patch(self, request, *args, **kwargs):
        try:
            fuzzer_id = kwargs.get('pk')
            fuzzer = Fuzzer.objects.get(id=fuzzer_id)
        except Exception as e:
            raise APIException(detail="Fuzzer not found", code=404) 
        if fuzzer.builtin:
            return self.update(request, *args, **kwargs)
        else:
            if 'fuzzer_zip' in request.FILES.get('fuzzer_zip'):
                try:
                    zip_file = request.FILES.get('fuzzer_zip')
                    zip_file_name = request.data['filename']

                    try:
                        bucket_name = configuration.get_value(
                            key_path="fuzzers.bucket", 
                            config=yaml.safe_load(fuzzer.project.configuration)
                        )
                    except Exception as e:
                        raise APIException("Failed to get bucket name from configuration", code=500)

                    try:
                        file =  {
                            "name": zip_file.name,
                            "content": base64.b64encode(zip_file.read()).decode('utf-8'),  # Encode bytes as base64 string
                            "content_type": zip_file.content_type
                        }
                        upload_fuzzer_to_bucket.delay(file, bucket_name)
                    except Exception as e:
                        raise APIException(f"Failed to upload fuzzer to bucket", code=500)
                    
                    request.data['blobstore_path'] = f"{bucket_name}/{zip_file_name}"
                    request.data['file_size'] = zip_file.size
                    
                    return self.update(request, *args, **kwargs)
                except Exception as e:
                    raise APIException(detail="An error occurred while updating the fuzzer", code=500)
            else:
                return self.update(request, *args, **kwargs)


class FuzzerDownloadView(APIView):
    """This view is used to explore coverage data for a project. Returns a JSON object which contains the html reports encoded as base64."""
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:           
            fuzzer_id = self.kwargs['pk']
            fuzzer = Fuzzer.objects.get(id=fuzzer_id)
        except Exception as e:
            raise APIException(detail="An error occurred while retrieving the fuzzer", code=500)
        
        if fuzzer.builtin:
            raise NotAcceptable(detail="Built-in fuzzers do not have source code", code=400)
        
        try:
            
            fuzzer_stream = get_fuzzer_from_cache.apply(args=[fuzzer.blobstore_path]).get()
            if not fuzzer_stream:
                    raise NotFound(detail="Report not found", code=404)
                
            # Ensure full file is available
            fuzzer_stream.seek(0, os.SEEK_END)
            file_size = fuzzer_stream.tell()
            fuzzer_stream.seek(0)
        
            response = FileResponse(fuzzer_stream, content_type="application/zip")
            response["Content-Length"] = file_size
            response["Content-Disposition"] = f'attachment; filename="{fuzzer.name}.zip"'
            return response
        
        except Exception as e:
            raise APIException(detail="Failed to generate coverage html report", code=500)
            
        
    