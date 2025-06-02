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

import json
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import yaml
from PinguApi.models import Bot, BotConfig
from rest_framework import status
from PinguApi.subtests.views.test_bot_api import init_test_bot
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase


def init_test_bot_config(bot):
        test_bot_config_yml = open("default_yml_configs/default_bot_config.yaml").read()
        botConfig = {'config_data': test_bot_config_yml,
               'bot': bot}
        botconfig_object = BotConfig.objects.create(**botConfig)
        botconfig_object.save()
        return botconfig_object
        
class BotConfigTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.bot_object = init_test_bot()
        self.botconfig_object = init_test_bot_config(self.bot_object)
    
    def test_register(self):
        test_bot_config_yml = open("default_yml_configs/default_bot_config.yaml").read()
        botConfig = {'config_data': test_bot_config_yml,
               'bot_id': self.bot_object.id}
        
        response = self.client.post(f'/api/botconfig/', data=botConfig, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_register_invalid_data(self):
        # Invalid YAML format
        botConfig = {'config_data': "Invalid YAML",
               'bot_id': self.bot_object.id}
        
        response = self.client.post(f'/api/botconfig/', data=botConfig, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid YAML value
        test_bot_config_yml = open("default_yml_configs/default_bot_config.yaml").read()
        parsed_config = yaml.safe_load(test_bot_config_yml)
        parsed_config['BOT_NAME'] = 123  # Invalid YAML value
        botConfig = {'config_data': yaml.dump(parsed_config),
        'bot_id': self.bot_object.id}
        
        response = self.client.post(f'/api/botconfig/', data=botConfig, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Unknown YAML Key
        test_bot_config_yml = open("default_yml_configs/default_bot_config.yaml").read()
        parsed_config = yaml.safe_load(test_bot_config_yml)
        parsed_config['UNKNOWN_KEY'] = "value"  # Unknown YAML Key
        botConfig = {'config_data': yaml.dump(parsed_config),
        'bot_id': self.bot_object.id}
        
        response = self.client.post(f'/api/botconfig/', data=botConfig, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        
    def test_get_botconfig(self):
        response = self.client.get(f'/api/botconfig/?id={self.botconfig_object.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_botconfig(self):
        response = self.client.delete(f'/api/botconfig/{self.botconfig_object.id}/')
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_patch_botconfig(self):
        test_bot_config_yml = open("default_yml_configs/default_bot_config.yaml").read()
        botConfig = {'config_data': test_bot_config_yml,
               'bot_id': self.bot_object.id}
        response = self.client.patch(f'/api/botconfig/{self.botconfig_object.id}/', 
                                     data=botConfig, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
            
