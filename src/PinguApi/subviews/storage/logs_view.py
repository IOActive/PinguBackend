import base64
from datetime import datetime
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import yaml
from PinguApi.handlers.storage_handlers.logs import LogsStorage
from PinguApi.serializers.storage.logs_serializer import FuzzerLogsSerializer, BotLogsSerializer
from rest_framework.exceptions import NotFound, APIException, ParseError, NotAcceptable

from PinguApi.submodels.fuzzer import Fuzzer
from PinguApi.submodels.project import Project
from PinguApi.submodels.job import Job
from PinguApi.tasks import download_logs, store_logs
from PinguApi.utilities import configuration
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics


class UploadLogsView(generics.GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not "log_type" in request.data:
            raise NotAcceptable(detail="Log type is required")
        
        log_type = request.data.get("log_type")
        
        if log_type == "bot":
            serializer = BotLogsSerializer(data=request.data)
            key_path = "logs.bot.bucket"
        elif log_type == "fuzzer":
            serializer = FuzzerLogsSerializer(data=request.data)
            key_path = "logs.fuzzer.bucket"
        else:
            raise NotAcceptable(detail="Invalid log type")
        
        if serializer.is_valid():
            data = serializer.validated_data
            job_id = data.get("job_id")
            task_id = data.get("task_id", "")
            fuzzer_id = data.get("fuzzer_id", "")
            files = data.get("files")
            project_id = data.get("project_id")
            
            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                raise NotFound(detail="Project does not exist.", code=404)
            
            if log_type == "fuzzer":
                try:
                    fuzzer = Fuzzer.objects.get(id=fuzzer_id)
                except Exception:
                    raise NotFound(detail="Fuzzer does not exist.", code=404)
            
            try:
                job = Job.objects.get(id=job_id)
            except Exception:
                raise NotFound(detail="Job does not exist.", code=404)
            
            # Get project bigquery bucket from project configuration
            try:
                bucket_name = configuration.get_value(key_path=key_path, config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)

            if log_type == "bot":
                storage_path = f"{job.name}/{task_id}/"
            elif log_type == "fuzzer":
                storage_path = f"{fuzzer.name}/{job.name}/"
                
            # Convert files to a serializable format
            files_data = [
                {
                    "name": file.name,
                    "content": base64.b64encode(file.read()).decode('utf-8'),  # Encode bytes as base64 string
                    "content_type": file.content_type
                }
                for file in files
            ]

            try:
                store_logs.delay(bucket_name, storage_path, files_data)
            except Exception as e:
                raise APIException("Failed to store logs", code=500)
            
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadLogsView(APIView):
    
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Download logs",
        manual_parameters=[
            openapi.Parameter('log_type', openapi.IN_QUERY, description="Type of log (bot or fuzzer)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('job_id', openapi.IN_QUERY, description="Job ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('task_id', openapi.IN_QUERY, description="Task ID", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('fuzzer_id', openapi.IN_QUERY, description="Fuzzer ID", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('project_id', openapi.IN_QUERY, description="Project ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('date', openapi.IN_QUERY, description="Date", type=openapi.TYPE_STRING, required=False),
        ],
        responses={200: 'Logs downloaded successfully', 400: 'Bad request', 404: 'Not found', 406: 'Not acceptable', 500: 'Internal server error'}
    )
    def get(self, request, *args, **kwargs):
        if not "log_type" in request.query_params:
            raise NotAcceptable(detail="Log type is required")
        
        log_type = request.query_params.get("log_type")
        
        if log_type == "bot":
            serializer = BotLogsSerializer(data=request.query_params.dict())
            key_path = "logs.bot.bucket"
        elif log_type == "fuzzer":
            serializer = FuzzerLogsSerializer(data=request.query_params.dict())
            key_path = "logs.fuzzer.bucket"
        else:
            raise NotAcceptable(detail="Invalid log type")
        
        if serializer.is_valid():
            data = serializer.validated_data
            job_id = data.get("job_id")
            task_id = data.get("task_id", "")
            fuzzer_id = data.get("fuzzer_id", "")
            project_id = data.get("project_id")
            date = data.get("date")

            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                raise NotFound(detail="Project does not exist.", code=404)
            
            if log_type == "fuzzer":
                try:
                    fuzzer = Fuzzer.objects.get(id=fuzzer_id)
                except Exception:
                    raise NotFound(detail="Fuzzer does not exist.", code=404)
            
            try:
                job = Job.objects.get(id=job_id)
            except Exception:
                raise NotFound(detail="Job does not exist.", code=404)
            
            try:
                bucket_name = configuration.get_value(key_path=key_path, config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)
            
            if date:
                dt = date.strftime("%Y-%m-%d")

            if log_type == "bot":
                storage_path = f"{job.id}/{task_id}/"
            elif log_type == "fuzzer":
                storage_path = f"{fuzzer.name}/{job.id}/{dt}/"

            try:
                logs_stream = download_logs.apply(args=[bucket_name, storage_path]).get()
            except Exception as e:
                raise APIException("Failed to download logs", code=500)

            # Create a response with the ZIP stream
            response = FileResponse(
                logs_stream,
                as_attachment=True,
                filename=f"{project.name}_{log_type}_logs.zip",
                content_type='application/zip'
            )
            
            return response
            
        else:
            raise ParseError(detail="Invalid Request", code=406)
