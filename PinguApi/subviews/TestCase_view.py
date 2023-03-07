from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from PinguApi.submodels.TestCase import TestCase
from PinguApi.serializers.TestCase_serializer import TestCaseSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.utils import EnablePartialUpdateMixin

class TestCase_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'job_id']
    
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TestCase.objects.all()
        job_id = self.request.query_params.get('job_id')
        id = self.request.query_params.get('id')
        if name is not None and id is not None:
            queryset = queryset.filter(job_id=job_id, id=id)
        elif name is not None:
            queryset = queryset.filter(job_id=job_id)
        elif id is not None:
            queryset = queryset.filter(id=id)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
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


