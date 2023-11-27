from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.utils.workQueue import create_queue, publish, get_queue_element
from PinguApi.subtests.test_Job import JobTests
from PinguApi.subtests.test_TestCase import TestCaseTests
from django.conf import settings

class TaskTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        self.test_job = JobTests.init_test_Job(self)
        self.test_tesetcase = TestCaseTests.init_test_TestCase(self)
        self.mock_tasks = self.init_mock_tasks()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_mock_tasks(self):
        queue_host = settings.QUEUE_HOST
        create_queue('tasks-Linux')
        task = {'job_id': str(self.test_job.id),
                'platform': 'Linux',
                'command': 'ls',
                'argument': '-l',
                }
        publish('tasks-linux', json.dumps(task))
        return task
            
    def test_add_libfuzz_task(self):
        task_test = {
            'job_id': str(self.test_job.id),
            'platform': 'Linux',
            'command': 'fuzz',
            'argument': 'libFuzzer',
        }
        
        response = self.client.post(f'/api/task/', data=task_test, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_blackbox_fuzz_task(self):
        task_test = {
            'job_id': str(self.test_job.id),
            'platform': 'Linux',
            'command': 'fuzz',
            'argument': 'blackFuzzer',
        }
        
        response = self.client.post(f'/api/task/', data=task_test, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_minimize_task(self):
        task_test = {
            'job_id': str(self.test_job.id),
            'platform': 'Linux',
            'command': 'minimize',
            'argument': str(self.test_tesetcase.id),
        }
        
        response = self.client.post(f'/api/task/', data=task_test, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_task(self):
        response = self.client.get(f'/api/task/?platform=Linux')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_read_tasks(self):
        response = self.client.get(f'/api/task/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
