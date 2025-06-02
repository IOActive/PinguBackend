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

from django.forms import ValidationError
from PinguApi.submodels.bot_config import BotConfig
from PinguApi.serializers.bot_config_serializer import BotConfigSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from src.PinguApi.utilities.enable_partial_update_mixin import EnablePartialUpdateMixin
import yaml
from rest_framework.exceptions import ParseError, NotAcceptable
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import logging
from src.PinguApi.utilities.configuration import verify_config
from decouple import config
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# Load your default configuration
with open('default_yml_configs/default_bot_config.yaml', 'r') as file:
    DEFAULT_BOT_CONFIG = yaml.safe_load(file)

class BotConfig_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', "bot"]
    queryset = BotConfig.objects.all()
    serializer_class = BotConfigSerializer
    
    def get(self, request, *args, **kwargs):
        data = request.query_params
        if 'default_config' in data:
            try:
                with open('default_yml_configs/default_bot_config.yaml', 'r') as f:
                    default_config = yaml.safe_load(f)
                    return Response({"config_data": default_config})
            except:
                raise ParseError(detail="failed to load default config", code=400)      
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        config_data = request.data.get('config_data')
        if not config_data:
            raise ParseError({"error": "config_data is required"})
        
        try:
            parsed_config = yaml.safe_load(config_data)
            verify_config(parsed_config, default_config=DEFAULT_BOT_CONFIG)

            # Generate Access Token
            try:
                user = User.objects.get(id=request.user.id)
                access_token = Token.objects.get_or_create(user=user)
                logger.info(f"Access token generated for user: {request.user.username}")
                
                parsed_config['PINGUAPI_HOST'] = config('PINGUAPI_HOST')
                parsed_config['PINGUAPI_KEY'] = access_token[0].key

            except Exception as e:
                logger.error(f"Failed to generate access token for user {request.user.username}: {e}")
        
        except ValidationError as e:
            raise ParseError(detail=f"Invalid YAML Format: {e}", code=400)
        except Exception as e:
            raise ParseError(detail=f"Failed to parse YAML: {e}", code=400)
         
        # Now you can use parsed_config in the create logic
        request.data['config_data'] = yaml.safe_dump(parsed_config)
        return self.create(request, *args, **kwargs)



class BotConfig_Update_Delete_APIView(EnablePartialUpdateMixin, 
                      generics.mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BotConfig.objects.all()
    serializer_class = BotConfigSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        config_data = request.data.get('config_data')
        if not config_data:
            raise NotAcceptable(detail="config_data is required", code=406)
        
        try:
            parsed_config = yaml.safe_load(config_data)
            verify_config(parsed_config, default_config=DEFAULT_BOT_CONFIG)
            request.data['config_data'] = yaml.safe_dump(parsed_config)
            return self.update(request, *args, **kwargs)
        except ValidationError as e:
            raise ParseError(detail=f"Invalid YAML Configuration: {e}", code=400)
        except Exception as e:
            raise ParseError(detail=f"Failed to parse YAML configuration: {e}", code=400)
        
