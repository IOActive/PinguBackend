from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.Job import Job

class JobTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Job = self.init_test_Job()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Job(self):
        job = {
            "name": "Test_job",
            "description": "Test_job",
            "project": "Test_job",
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "enabled": False,
            "archived": False,
            "platform": "Linux",
            "environment_string": "",
            "custom_binary_path": "",
            "custom_binary_filename": "",
            "custom_binary_revision": 1
        }
        Job_object = Job.objects.create(**job)
        Job_object.save()
        return Job_object
            
    def test_create_Jobs(self):
        job = {
            "name": "Test_job",
            "description": "Test_job",
            "project": "Test_job",
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "enabled": False,
            "archived": False,
            "platform": "Linux",
            "environment_string": "",
            "custom_binary_path": "",
            "custom_binary_filename": "",
            "custom_binary_revision": 1
        }
        
        response = self.client.post(f'/api/job/', data=job, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Jobs(self):
        response = self.client.get(f'/api/job/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_Job(self):
        response = self.client.get(f'/api/job/?id={self.test_Job.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_Job(self):
        job_update = {
            "description": "Test_job2",        }
        
        response = self.client.patch(f'/api/job/{self.test_Job.id}/', data=job_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['description'], "Test_job2")
