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

from django.db.models import Prefetch
from PinguApi.submodels.testcase import TestCase
from PinguApi.serializers.testcase_serializer import TestCaseSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin
from PinguApi.submodels.crash import Crash
from rest_framework_simplejwt.authentication import JWTAuthentication


class TestCase_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = TestCase.objects.prefetch_related(Prefetch('crash_testcase', queryset=Crash.objects.select_related('testcase'))).order_by('-timestamp')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'job', 'job__project', 'crash_testcase__crash_type', 'crash_testcase__crash_state', 'crash_testcase__security_flag']
        
    serializer_class = TestCaseSerializer

    #queryset = TestCase.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestCase_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


