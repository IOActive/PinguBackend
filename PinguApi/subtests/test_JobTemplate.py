from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.JobTemplate import JobTemplate

class JobTemplateTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_JobTemplate = self.init_test_JobTemplate()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_JobTemplate(self):
        jobtemplate = {
            "name": "test_jobtemplate",
            "environment_string": ""
        }
        JobTemplate_object = JobTemplate.objects.create(**jobtemplate)
        JobTemplate_object.save()
        return JobTemplate_object
            
    def test_create_JobTemplates(self):
        jobtemplate = {
            "name": "test_jobtemplate2",
            "environment_string": ""
        }
                
        response = self.client.put(f'/api/jobtemplate/', data=jobtemplate, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_JobTemplates(self):
        response = self.client.get(f'/api/jobtemplate/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_JobTemplate(self):
        response = self.client.get(f'/api/jobtemplate/?id={self.test_JobTemplate.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_JobTemplate(self):
        jobtemplate_update = {
            "name": "test_jobtemplate3",
        }
        
        response = self.client.patch(f'/api/jobtemplate/{self.test_JobTemplate.id}/', data=jobtemplate_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['name'], "test_jobtemplate3")
