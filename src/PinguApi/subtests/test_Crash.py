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
from PinguApi.submodels.Crash import Crash

class CrashTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Crash = self.init_test_Crash()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Crash(self):
        crash = {
            "crash_signal": -1,
            "exploitability": "true",
            "crash_time": "2023-03-07",
            "crash_hash": "dasdasda",
            "verified": False,
            "additional": "dadsa",
            "iteration": 1,
            "crash_type": "sadas",
            "crash_address": "dasd",
            "crash_state": "adsa",
            "crash_stacktrace": b"",
            "regression": "dasda",
            "security_severity": 1,
            "absolute_path": "dsadas",
            "security_flag": True,
            "reproducible_flag": False,
            "return_code": "-1",
            "gestures": {},
            "resource_list": {},
            "fuzzing_strategy": {},
            "should_be_ignored": False,
            "application_command_line": "sadsa",
            "unsymbolized_crash_stacktrace": b"",
            "crash_frame": {},
            "crash_info": "sdsads",
            "crash_revision": 1
        }
        Crash_object = Crash.objects.create(**crash)
        Crash_object.save()
        return Crash_object
            
    def test_create_Crashs(self):
        crash = {
            "crash_signal": -1,
            "exploitability": "true",
            "crash_time": "2023-03-07",
            "crash_hash": "dasdasda",
            "verified": False,
            "additional": "dadsa",
            "iteration": 1,
            "crash_type": "sadas",
            "crash_address": "dasd",
            "crash_state": "adsa",
            "crash_stacktrace": b"",
            "regression": "dasda",
            "security_severity": 1,
            "absolute_path": "dsadas",
            "security_flag": True,
            "reproducible_flag": False,
            "return_code": "-1",
            "gestures": {},
            "resource_list": {},
            "fuzzing_strategy": {},
            "should_be_ignored": False,
            "application_command_line": "sadsa",
            "unsymbolized_crash_stacktrace": b"",
            "crash_frame": {},
            "crash_info": "sdsads",
            "crash_revision": 1
        }
        
        response = self.client.put(f'/api/crash/', data=crash, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Crashes(self):
        response = self.client.get(f'/api/crash/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_Crash(self):
        response = self.client.get(f'/api/crash/?id={self.test_Crash.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_Crash(self):
        crash_update = {
            "crash_signal": 1,
        }
        response = self.client.patch(f'/api/crash/{self.test_Crash.id}/', data=crash_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['crash_signal'], 1)
