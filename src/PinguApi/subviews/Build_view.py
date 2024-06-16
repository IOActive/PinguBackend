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

from django.shortcuts import render

from django.http.response import JsonResponse

 
from PinguApi.submodels.Build import Build
from PinguApi.serializers.Build_serializer import BuildSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.utils.EnablePartialUpdateMixin import EnablePartialUpdateMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from PinguApi.tasks import upload_build_to_bucket, download_build_from_bucket, remove_build_from_bucket
from django.core.exceptions import ObjectDoesNotExist

import base64
class Build_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'filename', 'type']
    
    queryset = Build.objects.all()

    serializer_class = BuildSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            builds = self.filter_queryset(self.get_queryset())
            builds_page = self.paginate_queryset(builds)
            for build in builds_page:
                build_zip_stream = download_build_from_bucket.apply(args=[build.blobstore_path]).get()
                if build_zip_stream:
                    build.build_zip = base64.b64encode(build_zip_stream).decode('utf-8')
            serializer = BuildSerializer(builds, many=True)
            return self.get_paginated_response(serializer.data)
        except ObjectDoesNotExist as e:
            return JsonResponse({"results": {}}, safe=False)
            
    def post(self, request, *args, **kwargs):
        zip_file = base64.b64decode(request.data['build_zip'])
        zip_file_name = request.data['filename']
        build_type = request.data['type']
        blobstore_path, size_in_bytes = upload_build_to_bucket.apply(args=[zip_file, zip_file_name, build_type]).get()
        request.data['blobstore_path'] = blobstore_path
        request.data['file_size'] = size_in_bytes
        return self.create(request, *args, **kwargs)


class Build_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    
    def delete(self, request, *args, **kwargs):
        remove_build_from_bucket.apply(args=[self.get_object().blobstore_path]).get()
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.data['build_zip'] and request.data['build_zip'] != '':
            zip_file = base64.b64decode(request.data['build_zip'])
            zip_file_name = request.data['filename']
            blobstore_path, size_in_bytes = upload_build_to_bucket.apply(args=[zip_file, zip_file_name]).get()
            request.data['blobstore_path'] = blobstore_path
            request.data['file_size'] = size_in_bytes
        return self.update(request, *args, **kwargs)


