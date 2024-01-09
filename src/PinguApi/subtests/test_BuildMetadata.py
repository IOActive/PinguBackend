from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.BuildMetadata import BuildMetadata

class BuildMetadataTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_BuildMetadata = self.init_test_BuildMetadata()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_BuildMetadata(self):
        buildmetadata = {
            "revision": 1,
            "bad_build": False,
            "console_output": "dadsa",
            "bot_name": "test_bot",
            "symbols": "dasdad",
            "timestamp": datetime.now().strftime('%Y-%m-%d')
        }
        BuildMetadata_object = BuildMetadata.objects.create(**buildmetadata)
        BuildMetadata_object.save()
        return BuildMetadata_object
            
    def test_create_BuildMetadatas(self):
        buildmetadata = {
            "revision": 1,
            "bad_build": False,
            "console_output": "dadsa",
            "bot_name": "test_bot",
            "symbols": "dasdad",
            "timestamp": datetime.now().strftime('%Y-%m-%d')
        }
        
        response = self.client.put(f'/api/buildmetadata/', data=buildmetadata, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_BuildMetadatas(self):
        response = self.client.get(f'/api/buildmetadata/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_BuildMetadata(self):
        response = self.client.get(f'/api/buildmetadata/?id={self.test_BuildMetadata.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_BuildMetadata(self):
        buildmetadata_update = {
            "revision": 2
        }
        
        response = self.client.patch(f'/api/buildmetadata/{self.test_BuildMetadata.id}/', data=buildmetadata_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['revision'], 2)