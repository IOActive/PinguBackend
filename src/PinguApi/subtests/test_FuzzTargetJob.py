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
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.FuzzTargetJob import FuzzTargetJob

class FuzzTargetJobTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_FuzzTargetJob = self.init_test_FuzzTargetJob()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_FuzzTargetJob(self):
        fuzztargetjob = {
            "weight": 1,
            "last_run": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        FuzzTargetJob_object = FuzzTargetJob.objects.create(**fuzztargetjob)
        FuzzTargetJob_object.save()
        return FuzzTargetJob_object
            
    def test_create_FuzzTargetJobs(self):
        fuzztargetjob = {
            "weight": 1,
            "last_run": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
            
        response = self.client.put(f'/api/fuzztargetjob/', data=fuzztargetjob, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_FuzzTargetJobs(self):
        response = self.client.get(f'/api/fuzztargetjob/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_FuzzTargetJob(self):
        response = self.client.get(f'/api/fuzztargetjob/?id={self.test_FuzzTargetJob.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_FuzzTargetJob(self):
        fuzztargetjob_update = {
            "weight": 2,
        }
        
        response = self.client.patch(f'/api/fuzztargetjob/{self.test_FuzzTargetJob.id}/', data=fuzztargetjob_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['weight'], 2)
