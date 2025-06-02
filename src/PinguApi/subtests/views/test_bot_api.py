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

from datetime import datetime
from uuid import uuid4
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.bot import Bot
from PinguApi.submodels.task import Task
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_job_api import init_test_Job

def init_test_bot():
    bot = {'name': "test_bot",
            'platform': "Linux"}
    bot_object = Bot.objects.create(**bot)
    bot_object.save()
    return bot_object
class BotTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_bot = init_test_bot()
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
            
    def test_register(self):
        bot = {'name': "test_bot2",
               'platform': "Linux"}
        
        response = self.client.post(f'/api/bot/', data=bot, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_bots(self):
        response = self.client.get(f'/api/bot/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_bot(self):
        bot_name = 'test_bot'
        response = self.client.get(f'/api/bot/?name={bot_name}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_heartbeat(self):
        beat = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        heartbeat = {'name': 'luckycat', 'last_beat_time': beat, 'platform': 'Linux'}

        
        response = self.client.patch(f'/api/bot/{self.test_bot.id}/', data=heartbeat, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_bot_with_current_task(self):
        task = {
            "payload": "test payload",
            "status": "PENDING",
            "job_id": str(self.test_job.id)
        }
        task = Task.objects.create(**task)
        self.test_bot.current_task = task
        # update the bot with current task
        self.test_bot.save()
        
        response = self.client.get(f'/api/bot/?id={self.test_bot.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(result['results'][0]['current_task_id'] is not None)
