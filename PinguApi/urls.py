from django.urls import path 
from PinguApi import views 

urlpatterns = [
    path(r'swagger.json', views.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("job/", views.Job_List_Create_APIView.as_view(), name='job List Create'),
    path('job/<uuid:pk>/', views.Job_Update_Delete_APIView.as_view(), name="job update/delete"),
    path("bot/", views.Bot_List_Create_APIView.as_view(), name='Bot List Create'),
    path('bot/<uuid:pk>/', views.Bot_Update_Delete_APIView.as_view(), name="Bot update/delete"),
    path('api-token-auth/', views.CustomAuthToken.as_view())
]
