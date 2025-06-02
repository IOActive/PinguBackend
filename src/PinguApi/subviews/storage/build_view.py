import base64
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import yaml
from PinguApi.handlers.storage_handlers.build import BuildStorage
from PinguApi.serializers.storage.build_serializer import BuildSerializer
from rest_framework.exceptions import NotFound, APIException, ParseError, NotAcceptable

from PinguApi.submodels.project import Project
from PinguApi.tasks import download_build, get_build_list, get_build_size
from PinguApi.utilities import configuration
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

class BuildSizeView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get build size",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_QUERY, description="Project ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('build_type', openapi.IN_QUERY, description="Build type", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('file_path', openapi.IN_QUERY, description="File path", type=openapi.TYPE_STRING, required=False),
        ],
        responses={200: 'Build size retrieved successfully', 400: 'Bad request', 404: 'Not found', 500: 'Internal server error'}
    )
    def get(self, request, *args, **kwargs):
        serializer = BuildSerializer(data=request.query_params.dict())
        if serializer.is_valid():
            data = serializer.validated_data
            project_id = data.get("project_id")
            build_type = data.get("build_type")
            file_path = data.get("file_path", "")

            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                raise NotFound(detail="Project does not exist.", code=404)

            try:
                bucket_name = configuration.get_value(key_path=f"build.{build_type}.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)

            storage_path = f"{bucket_name}/{file_path}"

            try:
                build_size = get_build_size.apply(args=[bucket_name, storage_path]).get()
            except Exception as e:
                raise APIException("Failed to get build size", code=500)

            return Response({"build_size": build_size}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuildDownloadView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads

    def post(self, request, *args, **kwargs):
        serializer = BuildSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            project_id = data.get("project_id")
            build_type = data.get("build_type")
            file_path = data.get("file_path", "")

            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                raise NotFound(detail="Project does not exist.", code=404)

            try:
                bucket_name = configuration.get_value(key_path=f"build.{build_type}.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)

            try:
            
                build_stream = download_build.apply(args=[bucket_name, file_path]).get()
                if not build_stream:
                        raise NotFound(detail="Report not found", code=404)
                    
                # Ensure the stream is at the beginning
                build_stream.seek(0)
            
                response = FileResponse(build_stream, content_type="application/zip")
                response["Content-Disposition"] = f'attachment; filename="{project_id}.zip"'
                return response
        
            except Exception as e:
                raise APIException(detail="Failed to download build package", code=500)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuildListView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get build list",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_QUERY, description="Project ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('build_type', openapi.IN_QUERY, description="Build type", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('file_path', openapi.IN_QUERY, description="File path", type=openapi.TYPE_STRING, required=False),
        ],
        responses={200: 'Build list retrieved successfully', 400: 'Bad request', 404: 'Not found', 500: 'Internal server error'}
    )
    def get(self, request, *args, **kwargs):
        serializer = BuildSerializer(data=request.query_params.dict())
        if serializer.is_valid():
            data = serializer.validated_data
            project_id = data.get("project_id")
            build_type = data.get("build_type")

            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                raise NotFound(detail="Project does not exist.", code=404)

            try:
                bucket_name = configuration.get_value(key_path=f"build.{build_type}.bucket", config=yaml.safe_load(project.configuration))
            except Exception:
                raise APIException("Failed to get bucket name from configuration", code=500)

            try:
                build_list_bytes = get_build_list.apply(args=[bucket_name]).get()
                build_list_str = build_list_bytes.decode('utf-8')
                build_list = [item for item in build_list_str.split('\n') if item]
            except Exception as e:
                raise APIException("Failed to get build list", code=500)

            return Response({"build_list": build_list}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
