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

import re
import uuid
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import yaml
from PinguApi.tasks import upload_custom_binary_to_bucket, remove_custom_binary_from_bucket
import base64
from PinguApi.submodels.job import Job
from PinguApi.submodels.project import Project
from src.PinguApi.utilities import configuration
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, NotAcceptable, APIException

class CustomBinary_APIView(APIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def delete(self, request):
        data = request.query_params
        job_id = data['job_id']
        
        if 'job_id' not in data:
            response = Response({'success': False, 'msg': 'Job ID not specified'})
            response.status_code = 400
            return response
        else:
            job_id = data['job_id']
            job = Job.objects.get(id=job_id)
            
            bucket_name, blob_key = job.custom_binary_path.split("/")
            
            remove_custom_binary_from_bucket.apply(args=[blob_key, bucket_name]).get()
            
            job.custom_binary_filename = ""
            job.custom_binary_filename = ""
            job.custom_binary_path = ""
            
            regex = r"CUSTOM_BINARY"
            replacement = ""

            job.environment_string = re.sub(regex, replacement, job.environment_string)
            
            job.save()
                        
            response = Response({'success': True, 'msg': 'Binary uploaded'})

            response.status_code = 204
            return response
        
    
    def post(self, request):
        custom_binary_zip = request.FILES.get('custom_binary')
        job_id = request.data.get('job_id')
        
        if custom_binary_zip is None:
            raise NotAcceptable("Custom binary is required", code=406)
        
        elif job_id is None:
            raise NotAcceptable("Job ID is required", code=406)
        
        else:
            try:
                job = Job.objects.get(id=job_id)
            except ObjectDoesNotExist:
                raise NotFound(detail="Job not found", code=404)
            try:
                project = Project.objects.get(id=job.project.id)
            except ObjectDoesNotExist:
                raise NotFound(detail=f"Project with id {job.project} does not exist", code=404)
            
            blob_name = str(uuid.uuid4())
            
            try:
                bucket_name = configuration.get_value(key_path="blobs.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)
            
            try:
                file =  {
                    "name": blob_name,
                    "content": base64.b64encode(custom_binary_zip.read()).decode('utf-8'),  # Encode bytes as base64 string
                    "content_type": custom_binary_zip.content_type
                }
                upload_custom_binary_to_bucket.delay(file, bucket_name)
            except Exception as e:
                raise APIException(f"Failed to upload custom binary to bucket", code=500)
                                   
            job.custom_binary_filename = custom_binary_zip.name
            job.custom_binary_key = blob_name
            job.custom_binary_path = f"{bucket_name}/{blob_name}"
            job.environment_string += f"\nCUSTOM_BINARY = {custom_binary_zip.name}\n"
            
            job.save()
                        
            response = Response({'success': True, 'msg': 'Binary uploaded'})

            response.status_code = 201
            return response