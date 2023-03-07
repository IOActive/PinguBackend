from django.urls import path 
from PinguApi import views 
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path(r'swagger.json', views.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path("job/", views.Job_List_Create_APIView.as_view(), name='job List Create'),
    path('job/<uuid:pk>/', views.Job_Update_Delete_APIView.as_view(), name="job update/delete"),
    
    path("bot/", views.Bot_List_Create_APIView.as_view(), name='Bot List Create'),
    path('bot/<uuid:pk>/', views.Bot_Update_Delete_APIView.as_view(), name="Bot update/delete"),
    
    path("coverage/", views.Coverage_List_Create_APIView().as_view(), name='Coverage List Create'),
    path('coverage/<uuid:pk>/', views.Coverage_Update_Delete_APIView().as_view(), name="Coverage update/delete"),
    
    path("buildmetada/", views.BuildMetadata_List_Create_APIView().as_view(), name='Buildmetada List Create'),
    path('buildmetada/<uuid:pk>/', views.BuildMetadata_Update_Delete_APIView().as_view(), name="Buildmetada update/delete"),
    
    path("databundle/", views.DataBundle_List_Create_APIView.as_view(), name='Databundle List Create'),
    path('databundle/<uuid:pk>/', views.DataBundle_Update_Delete_APIView.as_view(), name="Databundle update/delete"),
    
    path("fuzzer/", views.Fuzzer_List_Create_APIView.as_view(), name='Fuzzer List Create'),
    path('fuzzer/<uuid:pk>/', views.Fuzzer_Update_Delete_APIView.as_view(), name="Fuzzer update/delete"),
    
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
    
    path('api-token-auth/', rest_framework_views.obtain_auth_token)

]
