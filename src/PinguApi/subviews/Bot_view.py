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
                    bot_logs_stream = download_bot_logs.apply(args=[str(bot.id)]).get()
                    if bot_logs_stream:
                        bot.bot_logs = base64.b64encode(bot_logs_stream).decode('utf-8')
                else:
                    bot.bot_logs = base64.b64encode('No logs available'.encode()).decode('utf-8')
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


