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

from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.tasks import upload_corpus_to_bucket
import base64
from PinguApi.models import Job
from PinguApi.submodels.Fuzzer import Fuzzer

class Corpus_APIView(APIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
    def post(self, request):
        body = request.data
        corpus_binary = body.get('corpus_binary')
        job_id = body.get('job_id')
        file_name = body.get('filename')
        engine_id = body.get('engine_id')
        fuzztarget_name = body.get('fuzztarget_name')
        
        required_fields = ('corpus_binary', 'file_name', 'job_id', 'engine_id', 'fuzztarget_name')

        if all(field is not None for field in required_fields):
            
            if file_name.split('.')[-1] != 'zip':
                response = Response({'success': False, 'msg': 'The corpus file needs to be a ZIP package'})
                response.status_code = 400
                return response
            
            else:
                job = Job.objects.get(id=job_id)
                fuzzer = Fuzzer.objects.get(id=engine_id)
                
                project_name = job.name
                fuzzzer_name = fuzzer.name
                
                file = base64.b64decode(corpus_binary.split(',')[-1])
                
                blobstore_path, size_in_bytes = upload_corpus_to_bucket.apply(args=[file, project_name, fuzzzer_name, fuzztarget_name]).get()
                    
                response = Response({'success': True, 'msg': f'Corpus Uploaded uploaded to {blobstore_path} '})

                response.status_code = 201
                return response
        else:
            response = Response({'success': False, 'msg': f"All required fields were not given: {', '.join([field for field in required_fields if not field])}"})
            response.status_code = 400
            return response