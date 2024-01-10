from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from PinguApi.submodels.Fuzzer import Fuzzer
from PinguApi.serializers.Fuzzer_serializer import FuzzerSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.utils.EnablePartialUpdateMixin import EnablePartialUpdateMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.tasks import upload_fuzzer_to_bucket, download_fuzzer_from_bucket, remove_fuzzer_from_bucket
from PinguApi.utils.Base64FileField import ZIPBase64File
from django.core.exceptions import ObjectDoesNotExist

import base64
class Fuzzer_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']
    
    queryset = Fuzzer.objects.all()

    serializer_class = FuzzerSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            if 'id' in request.query_params:
                # get the fuzzer from db and modify the fuzzer_zip field with the blobstore_path from the bucket
                fuzzer = Fuzzer.objects.get(id=request.query_params['id'])
                fuzzer_zip_stream = download_fuzzer_from_bucket.apply(args=[fuzzer.blobstore_path]).get()
                if fuzzer_zip_stream:
                    fuzzer.fuzzer_zip = base64.b64encode(fuzzer_zip_stream).decode('utf-8')
                serializer = FuzzerSerializer(fuzzer)
                return JsonResponse({"results": serializer.data}, safe=False)
            elif 'name' in request.query_params:
                # get the fuzzer from db and modify the fuzzer_zip field with the blobstore_path from the bucket
                fuzzer = Fuzzer.objects.get(name=request.query_params['name'])
                fuzzer_zip_stream = download_fuzzer_from_bucket.apply(args=[fuzzer.blobstore_path]).get()
                if fuzzer_zip_stream:
                    fuzzer.fuzzer_zip = base64.b64encode(fuzzer_zip_stream).decode('utf-8')
                serializer = FuzzerSerializer(fuzzer)
                return JsonResponse({"results": serializer.data}, safe=False)
            else:
                fuzzers = self.get_queryset()
                for fuzzer in fuzzers:
                    fuzzer_zip_stream = download_fuzzer_from_bucket.apply(args=[fuzzer.blobstore_path]).get()
                    if fuzzer_zip_stream:
                        fuzzer.fuzzer_zip = base64.b64encode(fuzzer_zip_stream).decode('utf-8')
                serializer = FuzzerSerializer(fuzzers, many=True)
                return JsonResponse({"results": serializer.data}, safe=False)
        except ObjectDoesNotExist as e:
            return JsonResponse({"results": {}}, safe=False)
            
    def post(self, request, *args, **kwargs):
        zip_file = base64.b64decode(request.data['fuzzer_zip'])
        zip_file_name = request.data['filename']
        blobstore_path, size_in_bytes = upload_fuzzer_to_bucket.apply(args=[zip_file, zip_file_name]).get()
        request.data['blobstore_path'] = blobstore_path
        request.data['file_size'] = size_in_bytes
        return self.create(request, *args, **kwargs)


class Fuzzer_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Fuzzer.objects.all()
    serializer_class = FuzzerSerializer
    
    def delete(self, request, *args, **kwargs):
        remove_fuzzer_from_bucket.apply(args=[self.get_object().blobstore_path]).get()
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.data['fuzzer_zip'] and request.data['fuzzer_zip'] != '':
            zip_file = base64.b64decode(request.data['fuzzer_zip'])
            zip_file_name = request.data['filename']
            blobstore_path, size_in_bytes = upload_fuzzer_to_bucket.apply(args=[zip_file, zip_file_name]).get()
            request.data['blobstore_path'] = blobstore_path
            request.data['file_size'] = size_in_bytes
        return self.update(request, *args, **kwargs)


