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
from PinguApi.subviews.job_view import Job_List_Create_APIView, Job_Update_Delete_APIView
from PinguApi.subviews.swagger_view import schema_view
from PinguApi.subviews.bot_view import Bot_List_Create_APIView, Bot_Update_Delete_APIView
from PinguApi.subviews.build_metadata_view import BuildMetadata_List_Create_APIView, BuildMetadata_Update_Delete_APIView
from PinguApi.subviews.coverage_view import Coverage_List_Create_APIView, Coverage_Update_Delete_APIView
from PinguApi.subviews.data_bundle_view import DataBundle_List_Create_APIView, DataBundle_Update_Delete_APIView
from PinguApi.subviews.fuzzer_view import Fuzzer_List_Create_APIView, Fuzzer_Update_Delete_APIView, FuzzerDownloadView
from PinguApi.subviews.fuzz_target_view import FuzzTarget_List_Create_APIView, FuzzTarget_Update_Delete_APIView
from PinguApi.subviews.fuzz_target_job_view import FuzzTargetJob_List_Create_APIView, FuzzTargetJob_Update_Delete_APIView
from PinguApi.subviews.Job_template_view import JobTemplate_List_Create_APIView, JobTemplate_Update_Delete_APIView
from PinguApi.subviews.statistic_view import Statistic_List_Create_APIView, Statistic_Update_Delete_APIView
from PinguApi.subviews.test_case_view import TestCase_List_Create_APIView, TestCase_Update_Delete_APIView
from PinguApi.subviews.test_case_variant_view import TestCaseVariant_List_Create_APIView, TestCaseVariant_Update_Delete_APIView
from PinguApi.subviews.trial_view import Trial_List_Create_APIView, Trial_Update_Delete_APIView
from PinguApi.subviews.crash_view import Crash_List_Create_APIView, Crash_Update_Delete_APIView
from PinguApi.subviews.custom_binary_view import CustomBinary_APIView
from PinguApi.subviews.corpus_view import Corpus_APIView
from PinguApi.subviews.build_view import Build_List_Create_APIView, Build_Update_Delete_APIView, BuildDownloadView as FrontBuildDownloadView
from PinguApi.subviews.task_view import Task_List_Create_APIView, Task_Update_Delete_APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from PinguApi.subviews.bot_config_view import BotConfig_List_Create_APIView, BotConfig_Update_Delete_APIView
from PinguApi.subviews.project_view import Project_List_Create_APIView, Project_Update_Delete_APIView
from PinguApi.subviews.fuzz_stats_view import Fuzz_Stats_List_Load_APIView
from PinguApi.subviews.crash_stats_view import CrashStats_List_Create_APIView
from PinguApi.subviews.coverage_explorer_view import CoverageDownloadView, CoverageExplorerView
# Storage views
from PinguApi.subviews.storage.corpus_view import CorpusUploadView, CorpusDownloadView
from PinguApi.subviews.storage.stats_view import StatsUploadView
from PinguApi.subviews.storage.coverage_view import CoverageUploadView
from PinguApi.subviews.storage.blobs_view import DownloadBlobView, ReadBlobView, BlobUploadView, DeleteBlobView
from PinguApi.subviews.storage.logs_view import UploadLogsView, DownloadLogsView
from PinguApi.subviews.storage.build_view import BuildSizeView, BuildDownloadView, BuildListView
from PinguApi.subviews.storage.dictionaries_view import DictionaryUploadView, DictionaryDownloadView, ListDictionariesView, DictionaryExistsView

# TODO: add fuzzer big query data view from bucket data. Should I store it in the DB?
