from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.Trial import Trial

class TrialTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Trial = self.init_test_Trial()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Trial(self):
        trial = {
            "app_name": "fdsf",
            "probability": 5,
            "app_args": "das"
        }
        Trial_object = Trial.objects.create(**trial)
        Trial_object.save()
        return Trial_object
            
    def test_create_Trials(self):
        trial = {
            "app_name": "fdsf",
            "probability": 5,
            "app_args": "das"
        }
        
        response = self.client.put(f'/api/trial/', data=trial, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Trials(self):
        response = self.client.get(f'/api/trial/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_Trial(self):
        response = self.client.get(f'/api/trial/?id={self.test_Trial.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_Trial(self):
        trial_update = {
            "probability": 10,
        }
        
        response = self.client.patch(f'/api/trial/{self.test_Trial.id}/', data=trial_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['probability'], 10)
