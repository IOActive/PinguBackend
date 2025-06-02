import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import yaml
from PinguApi.serializers.storage.corpus_serializer import CorpusTypes, CorpusUploadSerializer
from PinguApi.tasks import store_corpus, download_corpus
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.project import Project
from rest_framework.exceptions import NotFound, APIException, ParseError, ValidationError, NotAcceptable
from django.http import FileResponse, StreamingHttpResponse

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from PinguApi.utilities import configuration
from src.PinguApi.serializers.corpus_stats_serializer import CorpusStatsSerializer
class CorpusDownloadView(APIView):
    
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="project_id",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Project ID",
                required=True,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="fuzz_target_id",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Fuzz Target ID",
                required=True,
                type=openapi.TYPE_STRING
            ),
            
        ]
    )
    def get(self, request, *args, **kwargs):
        
        # Extract query parameters
        project_id = request.query_params.get('project_id')
        fuzz_target_id = request.query_params.get('fuzz_target_id')

        if not project_id or not fuzz_target_id:
            raise NotAcceptable(detail='Missing project_id or fuzz_target_id')

        # Validate project existence
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound(detail="Project does not exist.", code=404)

        # Validate fuzz target existence
        try:
            fuzz_target = FuzzTarget.objects.get(id=fuzz_target_id)
        except FuzzTarget.DoesNotExist:
            raise NotFound(detail="Fuzz target does not exist.", code=404)

        # Get project corpus bucket from project configuration
        try:
            bucket_name = configuration.get_value(key_path="corpus.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)
        # Construct the storage path (same as upload view)
        storage_path = f"{fuzz_target.fuzzer.name}_{fuzz_target.binary}"

        # Execute the download_corpus task synchronously
        result = download_corpus.apply(args=[bucket_name, storage_path])  # use_cache=True by default

        # Get the task result (BytesIO stream or None)
        zip_stream = result.get()

        if zip_stream is None:
            raise NotFound(detail="No corpus files found or failed to retrieve corpus.", code=404)

        # Create a response with the ZIP stream
        response = FileResponse(
            zip_stream,
            as_attachment=True,
            filename=f"corpus_{project.name}_{fuzz_target.fuzzer.name}_{fuzz_target.binary}.zip",
            content_type='application/zip'
        )
        
        # record new Corpus Stats
        stats = CorpusStatsSerializer(data={
            'size': zip_stream.getbuffer().nbytes,  # Use file size directly
            'project_id': project.id,
            'fuzzer_id': fuzz_target.fuzzer.id,
            'fuzzer_target_id': fuzz_target.id,
            'bucket_path': f"{fuzz_target.fuzzer.name}_{fuzz_target.binary}/"
        })
            
        if stats.is_valid():
            stats.save()
        else:
            raise APIException("Invalid corpus stats", code=500)

        return response

class CorpusUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    serializer_class = CorpusUploadSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
            try:
                serializer = CorpusUploadSerializer(data=request.data)
            except Exception as e:
                raise ParseError(detail="Invalid Request", code=406)
            
            if serializer.is_valid():
                files = serializer.validated_data['files']
                project_id = serializer.validated_data['project_id']
                fuzz_target_id = serializer.validated_data['fuzz_target_id']
                kind = serializer.validated_data.get('kind', CorpusTypes.CORPUS)
                
                try:
                    project = Project.objects.get(id=project_id)
                except Exception:
                    raise NotFound(detail="Project does not exist.", code=404)
                
                try:
                    fuzz_target = FuzzTarget.objects.get(id=fuzz_target_id)
                except Exception:
                    raise NotFound(detail="Fuzz target does not exist.", code=404)
                
                match kind:
                    case CorpusTypes.CORPUS.value:
                        key_path = "corpus.bucket"
                    case CorpusTypes.BACKUP.value:
                        key_path = "backup.bucket"
                    case CorpusTypes.SHARED.value:
                        key_path = "shared-corpus.bucket"
                    case CorpusTypes.QUARANTINE.value:
                        key_path = "quarantine.bucket"                        
                
                # Get project corpus bucket from project configuration
                try:
                    bucket_name = configuration.get_value(key_path=key_path, config=yaml.safe_load(project.configuration))
                except Exception:
                    raise APIException("Failed to get bucket name from configuration", code=500)
                
                storage_path = f"{fuzz_target.fuzzer.name}_{fuzz_target.binary}/"
                
                                                # Convert files to a serializable format
                files_data = [
                    {
                        "name": file.name,
                        "content": base64.b64encode(file.read()).decode('utf-8'),  # Encode bytes as base64 string
                        "content_type": file.content_type
                    }
                    for file in files
                ]
                    
                # Trigger async fuzzing task (optional)
                store_corpus.delay(bucket_name, storage_path, files_data)

                return Response({"message": "Corpus uploaded"}, status=201)
            
            raise ParseError(detail="Invalid Request", code=406)