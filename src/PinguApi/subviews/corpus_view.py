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
import yaml
from PinguApi.tasks import upload_corpus_to_bucket
import base64
from PinguApi.models import Job
from PinguApi.submodels.fuzzer import Fuzzer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException, NotAcceptable, NotFound

from PinguApi.utilities import configuration
from PinguApi.submodels.project import Project
from PinguApi.serializers.corpus_stats_serializer import CorpusStatsSerializer
from PinguApi.submodels.fuzz_target import FuzzTarget
from rest_framework.parsers import MultiPartParser, FormParser

class Corpus_APIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    
    def post(self, request):
        corpus_zip = request.FILES.get('corpus_binary')  # Get uploaded file
        job_id = request.data.get('job_id')
        file_name = request.data.get('filename')
        fuzzer_id = request.data.get('fuzzer_id')
        fuzztarget_name = request.data.get('fuzztarget_name')
        
        required_files = [job_id, file_name, fuzzer_id, fuzztarget_name]
        
        if all(required_files) and corpus_zip:
            
            if file_name.split('.')[-1] != 'zip':
                raise NotAcceptable(detail='The corpus file needs to be a ZIP package', code=406)
            
            try:
                job = Job.objects.get(id=job_id)
            except ObjectDoesNotExist:
                raise NotAcceptable(detail=f'Job with id {job_id} does not exist', code=406)
            try:
                fuzzer = Fuzzer.objects.get(id=fuzzer_id)
            except ObjectDoesNotExist:
                raise NotFound(detail=f"Fuzzer with id {fuzzer_id} does not exist")
            try:
                project = Project.objects.get(id=job.project.id)
            except ObjectDoesNotExist:
                raise NotFound(detail=f"Project with id {job.project.id} does not exist", code=406)
            try:
                fuzz_target = FuzzTarget.objects.get(binary=fuzztarget_name)
            except ObjectDoesNotExist:
                raise NotFound(detail=f"Fuzz target with name {fuzztarget_name} does not exist")

            try:
                bucket_name = configuration.get_value(key_path="corpus.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)
            
            
            bucket_path = f"{fuzzer.name}_{fuzztarget_name}"
            
            # Insert initial corpus stats
            stats = CorpusStatsSerializer(data={
                'size': corpus_zip.size,  # Use file size directly
                'project_id': project.id,
                'fuzzer_id': fuzzer.id,
                'fuzzer_target_id': fuzz_target.id,
                'bucket_path': bucket_path,
            })
            
            if stats.is_valid():
                stats.save()
            else:
                raise APIException("Invalid corpus stats", code=500)
            
            file =  {
                "name": corpus_zip.name,
                "content": base64.b64encode(corpus_zip.read()).decode('utf-8'),  # Encode bytes as base64 string
                "content_type": corpus_zip.content_type
            }
            # Save file temporarily or stream it to cloud storage
            upload_corpus_to_bucket.apply(args=[
                file,  # Read the actual file data
                bucket_name,
                bucket_path,]
            ).get
                
            response = Response({'success': True, 'message': f'Corpus Uploaded uploaded to {bucket_name} '})
            response.status_code = 201
            return response

        else:
            raise APIException(detail="Missing required fields", code=400)
