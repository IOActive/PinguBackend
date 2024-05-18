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
from PinguApi.subviews.CustomBinary_view import CustomBinary_APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# TODO: add fuzzer big query data view from bucket data. Should I store it in the DB?
