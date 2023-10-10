from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.db.models import Prefetch
from PinguApi.submodels.TestCase import TestCase
from PinguApi.serializers.TestCase_serializer import TestCaseSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.utils.EnablePartialUpdateMixin import EnablePartialUpdateMixin
from PinguApi.submodels.Crash import Crash
from rest_framework_simplejwt.authentication import JWTAuthentication


class TestCase_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = TestCase.objects.prefetch_related(Prefetch('crash_testcase', queryset=Crash.objects.select_related('testcase_id')))
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'job_id', 'job_id__project', 'crash_testcase__crash_type', 'crash_testcase__crash_state']
        
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


