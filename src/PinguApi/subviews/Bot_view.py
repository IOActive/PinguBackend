from django.shortcuts import render

from django.http.response import JsonResponse
 
from PinguApi.submodels.Bot import Bot
from PinguApi.serializers.Bot_serializer import BotSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from PinguApi.utils.EnablePartialUpdateMixin import EnablePartialUpdateMixin
import base64
from PinguApi.tasks import download_bot_logs
from django.core.exceptions import ObjectDoesNotExist
class Bot_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    
    def get(self, request, *args, **kwargs):
        
        try:
            bots = self.filter_queryset(self.get_queryset())
            bots_page = self.paginate_queryset(bots)
            for bot in bots_page:
                if bot.blobstore_log_path:
                    bot_logs_stream = download_bot_logs.apply(args=[str(bot.id), bot.blobstore_log_path]).get()
                    if bot_logs_stream:
                        bot.bot_logs = base64.b64encode(bot_logs_stream).decode('utf-8')
            serializer = BotSerializer(bots_page, many=True)
            return self.get_paginated_response(serializer.data)
        except ObjectDoesNotExist as e:
            return JsonResponse({"results": {}}, safe=False)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Bot_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

