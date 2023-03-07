from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class BotTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
            
    def test_register(self):
        bot = {'bot_name': "test_bot",
               'current_time': datetime.now().strftime('%Y-%m-%d'),
               'task_payload': "task_payload",
               'task_end_time': "2022-05-21",
               'last_beat_time': datetime.now().strftime('%Y-%m-%d'),
               'platform': "Linux"}
        
        response = self.client.put(f'/api/bot/', data=bot, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_bots(self):
        response = self.client.get(f'/api/bot/', format='json')
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_bot(self):
        bot_name = 'test_bot'
        response = self.client.get(f'/api/bot/?bot_name={bot_name}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_heartbeat(self):
        heartbeat = {
            "bot_name": "test_bot",
            "last_beat_time": datetime.now().strftime('%Y-%m-%d'),
            "task_status": "started"
        }
        response = self.client.patch(f'/api/bot/2188c36f-4d88-4060-8f03-60226fa452b1/', json=heartbeat, format=json)
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
