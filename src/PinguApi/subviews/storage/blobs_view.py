import base64
from datetime import datetime
import json
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import yaml
from PinguApi.submodels.project import Project
from rest_framework.exceptions import NotFound, APIException, ParseError, NotAcceptable
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from PinguApi.serializers.storage.blobs_serializer import GetBlobsSerializer, UploadBlobsSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from PinguApi.utilities import configuration
from src.PinguApi.tasks import download_blob, read_blob, write_blob, delete_blob


class BlobUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    serializer_class = UploadBlobsSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
            try:
                serializer = UploadBlobsSerializer(data=request.data)
            except Exception as e:
                raise ParseError(detail="Invalid Request", code=406)
            
            if serializer.is_valid():
                project_id = serializer.validated_data['project_id']
                key = serializer.validated_data['key']
                blob = serializer.validated_data['blob']
                metadata = ""
                if 'metadata' in serializer.validated_data:
                    metadata = json.loads(serializer.validated_data['metadata'])
            else:
                raise ParseError(detail='Invalid data')
            
            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                raise NotFound(detail="Project does not exist.", code=404)
            
            try:
                bucket_name = configuration.get_value(key_path="blobs.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)
            
            blob_data = {
                "name": blob.name,
                "content": base64.b64encode(blob.read()).decode('utf-8'),  # Encode bytes as base64 string
                "content_type": blob.content_type
            }
        
            try:
                write_blob.delay(bucket_name, key, blob_data, metadata)
            except Exception as e:
                raise APIException(detail="The blob could not be retrieved from the bucket.")
            
            return Response({"message": "Blob uploaded"}, status=201)


class ReadBlobView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetBlobsSerializer

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
                name="key",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Blob key name",
                required=True,
                type=openapi.TYPE_STRING
            ),
            
        ]
    )
    
    def get(self, request, *args, **kwargs):
        try:
            serializer = GetBlobsSerializer(data=request.query_params.dict())
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data['project_id']
            key = serializer.validated_data['key']
            
        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            bucket_name = configuration.get_value(key_path="blobs.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)
        
        try:
            blob_stream = read_blob.apply(args=[bucket_name, key]).get()
        except Exception as e:
            raise APIException(detail="The blob could not be retrieved from the bucket.")
        
        if blob_stream is None:
            raise NotFound(detail="No corpus files found or failed to retrieve corpus.", code=404)

        # Return the binary content directly
        return Response(
            blob_stream,
            content_type="application/octet-stream",  # Or "application/zip" if it’s a ZIP
            status=200
        )
        
        return response
            

class DownloadBlobView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetBlobsSerializer

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
                name="key",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Blob key name",
                required=True,
                type=openapi.TYPE_STRING
            ),
            
        ]
    )
    
    def get(self, request, *args, **kwargs):
        try:
            serializer = GetBlobsSerializer(data=request.query_params.dict())
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data['project_id']
            key = serializer.validated_data['key']
            
        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            bucket_name = configuration.get_value(key_path="blobs.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)
        
        try:
            blob_stream = download_blob.apply(args=[bucket_name, key]).get()
        except Exception as e:
            raise APIException(detail="The blob could not be retrieved from the bucket.")
        
        if blob_stream is None:
            raise NotFound(detail="No corpus files found or failed to retrieve corpus.", code=404)

        response = FileResponse(
            blob_stream,
            as_attachment=True,
            filename=key,
            content_type='application/octet-stream'
        )
        
        return response
            
class DeleteBlobView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetBlobsSerializer

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
                name="key",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Blob key name",
                required=True,
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    def delete(self, request, *args, **kwargs):
        try:
            serializer = GetBlobsSerializer(data=request.query_params.dict())
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data['project_id']
            key = serializer.validated_data['key']
            
        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            bucket_name = configuration.get_value(key_path="blobs.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)
        
        try:
            delete_blob.apply(args=[bucket_name, key]).get()
        except Exception as e:
            raise APIException(detail="The blob could not be deleted from the bucket.")
        
        return Response({"message": "Blob deleted"}, status=204)
