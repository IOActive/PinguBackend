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

from django.urls import path, include
from PinguApi import views 
from rest_framework.authtoken import views as rest_framework_views
from rest_framework_simplejwt import views as jwt_views
from PinguApi.subviews.authentication_view import LoginViewSet, RegistrationViewSet, RefreshViewSet

urlpatterns = [
    path(r'swagger.json', views.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path("job/", views.Job_List_Create_APIView.as_view(), name='job List Create'),
    path('job/<uuid:pk>/', views.Job_Update_Delete_APIView.as_view(), name="job update/delete"),
    
    path("bot/", views.Bot_List_Create_APIView.as_view(), name='Bot List Create'),
    path('bot/<uuid:pk>/', views.Bot_Update_Delete_APIView.as_view(), name="Bot update/delete"),
    
    path("coverage/", views.CoverageExplorerView().as_view(), name='Coverage Reports'),
    path('coverage/<uuid:pk>/download/', views.CoverageDownloadView().as_view(), name="Download Coverage artifacts"),
    
    path("buildmetadata/", views.BuildMetadata_List_Create_APIView().as_view(), name='Buildmetada List Create'),
    path('buildmetadata/<uuid:pk>/', views.BuildMetadata_Update_Delete_APIView().as_view(), name="Buildmetada update/delete"),
    
    path("databundle/", views.DataBundle_List_Create_APIView.as_view(), name='Databundle List Create'),
    path('databundle/<uuid:pk>/', views.DataBundle_Update_Delete_APIView.as_view(), name="Databundle update/delete"),
    
    path("fuzzer/", views.Fuzzer_List_Create_APIView.as_view(), name='Fuzzer List Create'),
    path('fuzzer/<uuid:pk>/', views.Fuzzer_Update_Delete_APIView.as_view(), name="Fuzzer update/delete"),
    path("fuzzer/<uuid:pk>/download", views.FuzzerDownloadView.as_view(), name="Download Fuzzer File"),
    
    path("fuzztarget/", views.FuzzTarget_List_Create_APIView.as_view(), name='Fuzztarget List Create'),
    path('fuzztarget/<uuid:pk>/', views.FuzzTarget_Update_Delete_APIView.as_view(), name="Fuzztarget update/delete"),
    
    path("fuzztargetjob/", views.FuzzTargetJob_List_Create_APIView.as_view(), name='FuzztargetJob List Create'),
    path('fuzztargetjob/<uuid:pk>/', views.FuzzTargetJob_Update_Delete_APIView.as_view(), name="FuzztargetJob update/delete"),
    
    path("jobtemplate/", views.JobTemplate_List_Create_APIView.as_view(), name='JobTemplate List Create'),
    path('jobtemplate/<uuid:pk>/', views.JobTemplate_Update_Delete_APIView.as_view(), name="JobTemplate update/delete"),
    
    path("stadistics/", views.Statistic_List_Create_APIView.as_view(), name='Stadistics List Create'),
    path('stadistics/<uuid:pk>/', views.Statistic_Update_Delete_APIView.as_view(), name="Stadistics update/delete"),
    
    path("testcase/", views.TestCase_List_Create_APIView.as_view(), name='Testcase List Create'),
    path('testcase/<uuid:pk>/', views.TestCase_Update_Delete_APIView.as_view(), name="Testcase update/delete"),
    
    path("testcasevariant/", views.TestCaseVariant_List_Create_APIView.as_view(), name='TestCaseVariant List Create'),
    path('testcasevariant/<uuid:pk>/', views.TestCaseVariant_Update_Delete_APIView.as_view(), name="TestCaseVariant update/delete"),

    path("trial/", views.Trial_List_Create_APIView.as_view(), name='Trial List Create'),
    path('trial/<uuid:pk>/', views.Trial_Update_Delete_APIView.as_view(), name="Trial update/delete"),

    path("crash/", views.Crash_List_Create_APIView.as_view(), name='Crash List Create'),
    path('crash/<uuid:pk>/', views.Crash_Update_Delete_APIView.as_view(), name="Crash update/delete"),
    
    path('api-token-auth/', rest_framework_views.obtain_auth_token),
    
    path('task/', views.Task_List_Create_APIView.as_view(), name='Task Add/Fetch'),
    path('task/<uuid:pk>/', views.Task_Update_Delete_APIView.as_view(), name="Task update/delete"),
    
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(('PinguApi.routers', 'PinguApi'), namespace='core-api')),
    
    path('custom_binary/', views.CustomBinary_APIView.as_view(), name='custom_binary'),
    
    path('corpus/', views.Corpus_APIView.as_view(), name="corpus upload"),
    
    path("build/", views.Build_List_Create_APIView.as_view(), name='Build List Create'),
    path('build/<uuid:pk>/', views.Build_Update_Delete_APIView.as_view(), name="Build update/delete"),
    path('build/<uuid:pk>/download/', views.FrontBuildDownloadView.as_view(), name="Build Download"),
    
    path("botconfig/", views.BotConfig_List_Create_APIView.as_view(), name='Bot Config List Create'),
    path('botconfig/<uuid:pk>/', views.BotConfig_Update_Delete_APIView.as_view(), name="Bot Config update/delete"),
    
    path("project/", views.Project_List_Create_APIView.as_view(), name='Project List Create'),
    path('project/<uuid:pk>/', views.Project_Update_Delete_APIView.as_view(), name="Project update/delete"),
    
    path("fuzzer_stats/", views.Fuzz_Stats_List_Load_APIView.as_view(), name='Fuzzer Stats GET LAUCH_LOADER'),
    path("crash_stats/", views.CrashStats_List_Create_APIView.as_view(), name="Crash Stats List Create"),
    
    # storage apis
    path('storage/corpus/upload/', views.CorpusUploadView.as_view(), name='Storage Corpus Upload'),
    path('storage/corpus/download/', views.CorpusDownloadView.as_view(), name='Corpus Download from Storage'),
    
    path('storage/stats/upload/', views.StatsUploadView.as_view(), name='Storage Stats Upload'),
    
    path('storage/coverage/upload/', views.CoverageUploadView.as_view(), name='Storage Coverage Upload'),
    
    path('storage/blobs/download/', views.DownloadBlobView.as_view(), name='Storage Download Blob'),
    path('storage/blobs/read/', views.ReadBlobView.as_view(), name='Storage Read Blob content'),
    path('storage/blobs/upload/', views.BlobUploadView.as_view(), name='Storage Upload Blob content'),
    path('storage/blobs/delete/', views.DeleteBlobView.as_view(), name='Storage Delete Blob content'),

    
    path('storage/logs/upload/', views.UploadLogsView.as_view(), name='Storage Logs Upload'),
    path('storage/logs/download/', views.DownloadLogsView.as_view(), name='Storage Logs Download'),
    
    path('storage/builds/size/', views.BuildSizeView.as_view(), name='Storage Build Size'),
    path('storage/builds/download/', views.BuildDownloadView.as_view(), name='Storage Build Download'),
    path('storage/builds/list/', views.BuildListView.as_view(), name='Storage Build List'),
    
    path('storage/dictionaries/upload/', views.DictionaryUploadView.as_view(), name='Storage Dictionary Upload'),
    path('storage/dictionaries/download/', views.DictionaryDownloadView.as_view(), name='Storage Dictionary Download'),
    path('storage/dictionaries/list/', views.ListDictionariesView.as_view(), name='Storage Dictionaries List'),
    path('storage/dictionaries/exists/', views.DictionaryExistsView.as_view(), name='Storage Dictionary Exists'),

]
