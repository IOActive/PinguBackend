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
from PinguApi.submodels.TestCaseVariant import TestCaseVariant

class TestCaseVariantTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_TestCaseVariant = self.init_test_TestCaseVariant()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_TestCaseVariant(self):
        testcasevariant = {
            "status": 1,
            "revision": 1,
            "crash_type": "das",
            "crash_state": "dasda",
            "security_flag": False,
            "is_similar": False,
            "reproducer_key": "dsada",
            "platform": "Linux"
        }
        TestCaseVariant_object = TestCaseVariant.objects.create(**testcasevariant)
        TestCaseVariant_object.save()
        return TestCaseVariant_object
            
    def test_create_TestCaseVariants(self):
        testcasevariant = {
            "status": 1,
            "revision": 1,
            "crash_type": "das",
            "crash_state": "dasda",
            "security_flag": False,
            "is_similar": False,
            "reproducer_key": "dsada",
            "platform": "Linux"
        }
   
        response = self.client.put(f'/api/testcasevariant/', data=testcasevariant, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_TestCaseVariants(self):
        response = self.client.get(f'/api/testcasevariant/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_TestCaseVariant(self):
        response = self.client.get(f'/api/testcasevariant/?id={self.test_TestCaseVariant.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_TestCaseVariant(self):
        testcasevariant_update = {
            "revision": 2
        }
        
        response = self.client.patch(f'/api/testcasevariant/{self.test_TestCaseVariant.id}/', data=testcasevariant_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['revision'], 2)
