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
import re
import uuid
from django.shortcuts import render
import json
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from PinguApi.utils.workQueue import create_queue, publish, get_queue_element, queue_exists, read_queue_elements
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.tasks import upload_custom_binary_to_bucket, download_custom_binary_from_bucket, remove_custom_binary_from_bucket
from PinguApi.utils.Base64FileField import ZIPBase64File
from django.core.exceptions import ObjectDoesNotExist
import base64
from PinguApi.models import Job

class CustomBinary_APIView(APIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
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
            remove_custom_binary_from_bucket.apply(args=[job.custom_binary_path]).get()
            
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
        body = request.data
        custom_binanry = body.get('custom_binary')
        job_id = body.get('job_id')
        file_name = body.get('filename')
        
        if custom_binanry is None and file_name:
            response = Response({'success': False, 'msg': 'Custom binary not specified'})
            response.status_code = 400
            return response
        
        elif job_id is None:
            response = Response({'success': False, 'msg': 'Job ID not specified'})
            response.status_code = 400
            return response
        
        else:
            job = Job.objects.get(id=job_id)
            
            file = base64.b64decode(custom_binanry.split(',')[-1])
            
            blob_name = str(uuid.uuid4())
            blobstore_path, size_in_bytes = upload_custom_binary_to_bucket.apply(args=[file, blob_name]).get()
                       
            job.custom_binary_filename = file_name
            job.custom_binary_key = blob_name
            job.custom_binary_path = blobstore_path
            job.environment_string += f"\nCUSTOM_BINARY = {file_name}\n"
            
            job.save()
                        
            response = Response({'success': True, 'msg': 'Binary uploaded'})

            response.status_code = 201
            return response