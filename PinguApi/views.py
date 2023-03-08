from django.shortcuts import render

# Create your views here.
from PinguApi.subviews.Job_view import Job_List_Create_APIView, Job_Update_Delete_APIView
from PinguApi.subviews.swagger_view import schema_view
from PinguApi.subviews.Bot_view import Bot_List_Create_APIView, Bot_Update_Delete_APIView
from PinguApi.subviews.BuildMetadata_view import BuildMetadata_List_Create_APIView, BuildMetadata_Update_Delete_APIView
from PinguApi.subviews.Coverage_view import Coverage_List_Create_APIView, Coverage_Update_Delete_APIView
from PinguApi.subviews.DataBundle_view import DataBundle_List_Create_APIView, DataBundle_Update_Delete_APIView
from PinguApi.subviews.Fuzzer_view import Fuzzer_List_Create_APIView, Fuzzer_Update_Delete_APIView
from PinguApi.subviews.FuzzTarget_view import FuzzTarget_List_Create_APIView, FuzzTarget_Update_Delete_APIView
from PinguApi.subviews.FuzzTargetJob_view import FuzzTargetJob_List_Create_APIView, FuzzTargetJob_Update_Delete_APIView
from PinguApi.subviews.JobTemplate_view import JobTemplate_List_Create_APIView, JobTemplate_Update_Delete_APIView
from PinguApi.subviews.Statistic_view import Statistic_List_Create_APIView, Statistic_Update_Delete_APIView
from PinguApi.subviews.TestCase_view import TestCase_List_Create_APIView, TestCase_Update_Delete_APIView
from PinguApi.subviews.TestCaseVariant_view import TestCaseVariant_List_Create_APIView, TestCaseVariant_Update_Delete_APIView
from PinguApi.subviews.Trial_view import Trial_List_Create_APIView, Trial_Update_Delete_APIView
from PinguApi.subviews.Crash_view import Crash_List_Create_APIView, Crash_Update_Delete_APIView
from PinguApi.subviews.Task_view import Task_APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


'''
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        '''