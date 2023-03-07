from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.DataBundle import DataBundle

class DataBundleTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_DataBundle = self.init_test_DataBundle()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_DataBundle(self):
        databundle = {
            "name": "test_databundle",
            "bucket_name": "adsad",
            "source": "dasda",
            "is_local": False,
            "timestamp": "2023-03-07",
            "sync_to_worker": True
        }
        DataBundle_object = DataBundle.objects.create(**databundle)
        DataBundle_object.save()
        return DataBundle_object
            
    def test_create_DataBundles(self):
        databundle = {
            "name": "test_databundle",
            "bucket_name": "adsad",
            "source": "dasda",
            "is_local": False,
            "timestamp": "2023-03-07",
            "sync_to_worker": True
        }
        
        response = self.client.put(f'/api/databundle/', data=databundle, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_DataBundles(self):
        response = self.client.get(f'/api/databundle/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_DataBundle(self):
        response = self.client.get(f'/api/databundle/?id={self.test_DataBundle.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_DataBundle(self):
        databundle_update = {
            "is_local": True,
        }
        
        response = self.client.patch(f'/api/databundle/{self.test_DataBundle.id}/', data=databundle_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['is_local'], True)
