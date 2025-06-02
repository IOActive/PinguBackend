import base64
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import yaml
from PinguApi.handlers.storage_handlers.blobs import BlobsStorage
from rest_framework.exceptions import NotFound, APIException, ParseError, NotAcceptable
from PinguApi.submodels.project import Project
from PinguApi.utilities import configuration
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from PinguApi.tasks import upload_dictionary, download_dictionary, list_dictionaries, dictionary_exists
from PinguApi.serializers.storage.dictionaries_serializer import GetDictionarySerializer, UploadDictionarySerializer
from PinguApi.submodels.fuzz_target import FuzzTarget

class DictionaryUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Allow multipart form uploads
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        try:
            serializer = UploadDictionarySerializer(data=request.data)
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data.get('project_id')
            fuzztarget_id = serializer.validated_data.get('fuzztarget_id')
            dictionary_file = serializer.validated_data.get('dictionary')
        else:
            raise ParseError(detail='Invalid Request')

        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            fuzztarget = FuzzTarget.objects.get(id=fuzztarget_id)
        except Exception:
            raise NotFound(detail="Fuzztarget does not exist.", code=404)

        try:
            bucket_name = configuration.get_value(key_path="dictionaries.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)

        file_data = {
            "name": dictionary_file.name,
            "content": base64.b64encode(dictionary_file.read()).decode('utf-8'),  # Encode bytes as base64 string
            "content_type": dictionary_file.content_type
        }
        
        storage_path = f"{fuzztarget.fuzzer.name}_{fuzztarget.binary}"

        try:
            upload_dictionary.delay(bucket_name, storage_path, file_data)
        except Exception as e:
            raise APIException("Failed to upload dictionary", code=500)

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)

class DictionaryDownloadView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Download dictionary",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_QUERY, description="Project ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('fuzztarget_id', openapi.IN_QUERY, description="Fuzz Target ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('dictionary_name', openapi.IN_QUERY, description="Dictionary name", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: 'Dictionary downloaded successfully', 400: 'Bad request', 404: 'Not found', 500: 'Internal server error'}
    )
    def get(self, request, *args, **kwargs):
        
        try:
            serializer = GetDictionarySerializer(data=request.query_params.dict())
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data.get('project_id', '')
            fuzztarget_id = serializer.validated_data.get('fuzztarget_id', '')
            dictionary_name = serializer.validated_data.get('dictionary_name')
        else:
            raise ParseError(detail='Invalid Request')
        
        if not dictionary_name:
            raise ParseError(detail='Invalid Request')

        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            fuzztarget = FuzzTarget.objects.get(id=fuzztarget_id)
        except Exception:
            raise NotFound(detail="Fuzztarget does not exist.", code=404)

        try:
            bucket_name = configuration.get_value(key_path="dictionaries.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)

        storage_path = f"{fuzztarget.fuzzer.name}_{fuzztarget.binary}"
        
        try:
            dictionary_stream = download_dictionary.apply(args=[bucket_name, storage_path, dictionary_name]).get()
        except Exception as e:
            raise APIException("Failed to download dictionary", code=404)
        
        response = FileResponse(
            dictionary_stream,
            as_attachment=True,
            filename=dictionary_name,
            content_type='application/octet-stream'
        )
        
        return response

class DictionaryExistsView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Check if dictionary exists",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_QUERY, description="Project ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('fuzztarget_id', openapi.IN_QUERY, description="Fuzz Target ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('dictionary_name', openapi.IN_QUERY, description="Dictionary name", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: 'Dictionary exists', 404: 'Dictionary not found'}
    )
    def get(self, request, *args, **kwargs):
        
        try:
            serializer = GetDictionarySerializer(data=request.query_params)
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data.get('project_id', '')
            fuzztarget_id = serializer.validated_data.get('fuzztarget_id', '')
            dictionary_name = serializer.validated_data.get('dictionary_name')
        else:
            raise ParseError(detail='Invalid Request')
        
        if not dictionary_name:
            raise ParseError(detail='Invalid Request')

        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            fuzztarget = FuzzTarget.objects.get(id=fuzztarget_id)
        except Exception:
            raise NotFound(detail="Fuzztarget does not exist.", code=404)

        try:
            bucket_name = configuration.get_value(key_path="dictionaries.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)

        storage_path = f"{fuzztarget.fuzzer.name}_{fuzztarget.binary}"
        
        exists = dictionary_exists.apply(args=[bucket_name, storage_path, dictionary_name]).get()

        if exists:
            return Response({"status": "exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)

class ListDictionariesView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List dictionaries",
        manual_parameters=[
            openapi.Parameter('project_id', openapi.IN_QUERY, description="Project ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('fuzztarget_id', openapi.IN_QUERY, description="Fuzz Target ID", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: 'Dictionaries listed successfully', 400: 'Bad request', 404: 'Not found', 500: 'Internal server error'}
    )
    def get(self, request, *args, **kwargs):
        
        try:
            serializer = GetDictionarySerializer(data=request.query_params)
        except Exception as e:
            raise ParseError(detail="Invalid Request", code=406)
        
        if serializer.is_valid():
            project_id = serializer.validated_data.get('project_id', '')
            fuzztarget_id = serializer.validated_data.get('fuzztarget_id', '')
        else:
            raise ParseError(detail='Invalid Request')

        try:
            project = Project.objects.get(id=project_id)
        except Exception:
            raise NotFound(detail="Project does not exist.", code=404)
        
        try:
            fuzztarget = FuzzTarget.objects.get(id=fuzztarget_id)
        except Exception:
            raise NotFound(detail="Fuzztarget does not exist.", code=404)

        try:
            bucket_name = configuration.get_value(key_path="dictionaries.bucket", config=yaml.safe_load(project.configuration))
        except Exception:
            raise APIException("Failed to get bucket name from configuration", code=500)

        storage_path = f"{fuzztarget.fuzzer.name}_{fuzztarget.binary}"
        
        dictionaries = list_dictionaries.apply(args=[bucket_name, storage_path]).get()

        return Response({"dictionaries": dictionaries}, status=status.HTTP_200_OK)


