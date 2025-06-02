import base64
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import yaml
from PinguApi.tasks import store_stats
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.project import Project
from rest_framework.exceptions import NotFound, APIException, ParseError, NotAcceptable
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from PinguApi.utilities import configuration
from PinguApi.serializers.storage.stats_serializer import StatsUploadSerializer
from PinguApi.submodels.job import Job
from django.utils import timezone

COVERAGE_INFORMATION_DATE_FORMAT = '%Y-%m-%d'

class StatsUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    serializer_class = StatsUploadSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
            try:
                serializer = StatsUploadSerializer(data=request.data)
            except Exception as e:
                raise ParseError(detail="Invalid Request", code=406)
            
            if serializer.is_valid():
                files = serializer.validated_data['files']
                project_id = serializer.validated_data['project_id']
                fuzz_target_id = serializer.validated_data['fuzz_target_id']
                job_id = serializer.validated_data['job_id']
                kind = serializer.validated_data['kind']
                                
                try:
                    project = Project.objects.get(id=project_id)
                except Exception:
                    raise NotFound(detail="Project does not exist.", code=404)
                
                try:
                    fuzz_target = FuzzTarget.objects.get(id=fuzz_target_id)
                except Exception:
                    raise NotFound(detail="Fuzz target does not exist.", code=404)
                
                try:
                    job = Job.objects.get(id=job_id)
                except Exception as e:
                    raise NotFound(detail="Job does not exists")
                
                # Get project bigquery bucket from project configuration
                try:
                    bucket_name = configuration.get_value(key_path="bigquery.bucket", config=yaml.safe_load(project.configuration))
                except Exception:
                    raise APIException("Failed to get bucket name from configuration", code=500)
                
                current_time = datetime.now()
                current_time.replace(tzinfo=timezone.get_current_timezone())
                formatted_date = current_time.strftime("%Y-%m-%d")                
                
                storage_path = f"{fuzz_target.fuzzer.id}_{fuzz_target.binary}/{job.id}/{kind}/{formatted_date}/"
                    
                # Trigger async fuzzing task (optional)
                #store_stats.apply(args=[bucket_name, storage_path, files]).get()
                
                                # Convert files to a serializable format
                files_data = [
                    {
                        "name": file.name,
                        "content": base64.b64encode(file.read()).decode('utf-8'),  # Encode bytes as base64 string
                        "content_type": file.content_type
                    }
                    for file in files
                ]
                
                #store_stats.apply(args=[bucket_name, storage_path, files_data]).get()
                store_stats.delay(bucket_name, storage_path, files_data)

                return Response({"message": "Stats uploaded"}, status=201)
            
            raise ParseError(detail="Invalid Request", code=406)