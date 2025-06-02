import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import yaml
from PinguApi.tasks import store_coverage
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.project import Project
from rest_framework.exceptions import NotFound, APIException, ParseError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from PinguApi.utilities import configuration
from PinguApi.serializers.storage.coverage_serializer import CoverageUploadSerializer

class CoverageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    serializer_class = CoverageUploadSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
            try:
                serializer = CoverageUploadSerializer(data=request.data)
            except Exception as e:
                raise ParseError(detail="Invalid Request", code=406)
            
            if serializer.is_valid():
                files = serializer.validated_data['files']
                project_id = serializer.validated_data['project_id']
                fuzz_target_id = serializer.validated_data['fuzz_target_id']
                                
                try:
                    project = Project.objects.get(id=project_id)
                except Exception:
                    raise NotFound(detail="Project does not exist.", code=404)
                
                try:
                    fuzz_target = FuzzTarget.objects.get(id=fuzz_target_id)
                except Exception:
                    raise NotFound(detail="Fuzz target does not exist.", code=404)
                
                # Get project bigquery bucket from project configuration
                try:
                    bucket_name = configuration.get_value(key_path="coverage.bucket", config=yaml.safe_load(project.configuration))
                except Exception:
                    raise APIException("Failed to get bucket name from configuration", code=500)
                
                storage_path = f"{fuzz_target.fuzzer.name}_{fuzz_target.binary}/"
                    
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
                
                store_coverage.delay(bucket_name, storage_path, files_data)

                return Response({"message": "Stats uploaded"}, status=201)
            
            raise ParseError(detail="Invalid Request", code=406)