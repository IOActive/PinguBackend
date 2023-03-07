from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.Bot import Bot

class BotTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_bot = self.init_test_bot()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_bot(self):
        bot = {'bot_name': "test_bot",
               'task_payload': "task_payload",
               'task_end_time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
               'last_beat_time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
               'platform': "Linux"}
        bot_object = Bot.objects.create(**bot)
        bot_object.save()
        return bot_object
            
    def test_register(self):
        bot = {'bot_name': "test_bot2",
               'task_payload': "task_payload",
               'task_end_time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
               'last_beat_time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
               'platform': "Linux"}
        
        response = self.client.put(f'/api/bot/', data=bot, format='json')
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
        response = self.client.get(f'/api/bot/?bot_name={bot_name}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_heartbeat(self):
        beat = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        heartbeat = {
            "last_beat_time": beat,
        }
        
        response = self.client.patch(f'/api/bot/{self.test_bot.id}/', data=heartbeat, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['last_beat_time'], beat)
