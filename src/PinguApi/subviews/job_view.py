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

from PinguApi.submodels.job import Job
from PinguApi.serializers.job_serializer import JobSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin

class Job_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'project']
    
    serializer_class = JobSerializer
    
    queryset = Job.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Job_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


