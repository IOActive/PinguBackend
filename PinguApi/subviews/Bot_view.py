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
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            if 'id' in request.query_params:
                bot = Bot.objects.get(id=request.query_params['id'])
                if bot.blobstore_log_path:
                    bot_logs_stream = download_bot_logs.apply(args=[bot.blobstore_log_path]).get()
                    bot.bot_logs = base64.b64encode(bot_logs_stream).decode('utf-8')
                serializer = BotSerializer(bot)
                return JsonResponse({"results": serializer.data}, safe=False)
            elif 'name' in request.query_params:
                bot = Bot.objects.get(name=request.query_params['name'])
                if bot.blobstore_log_path:
                    bot_logs_stream = download_bot_logs.apply(args=[bot.blobstore_log_path]).get()
                    bot.bot_logs = base64.b64encode(bot_logs_stream).decode('utf-8')
                serializer = BotSerializer(bot)
                return JsonResponse({"results": serializer.data}, safe=False)
            else:
                bots = self.get_queryset()
                for bot in bots:
                    if bot.blobstore_log_path:
                        bot_logs_stream = download_bot_logs.apply(args=[bot.blobstore_log_path]).get()
                        bot.bot_logs = base64.b64encode(bot_logs_stream).decode('utf-8')
                serializer = BotSerializer(bots, many=True)
                return JsonResponse({"results": serializer.data}, safe=False)
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


