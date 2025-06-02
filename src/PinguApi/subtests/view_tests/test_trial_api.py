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

import json
from rest_framework import status
from rest_framework.authtoken.models import Token

from PinguApi.submodels.trial import Trial
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase

def init_test_Trial():
        trial = {
            "app_name": "fdsf",
            "probability": 5,
            "app_args": "das"
        }
        Trial_object = Trial.objects.create(**trial)
        Trial_object.save()
        return Trial_object
class TrialTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Trial = init_test_Trial()

    def test_create_Trials(self):
        trial = {
            "app_name": "fdsf",
            "probability": 5,
            "app_args": "das"
        }
        
        response = self.client.post(f'/api/trial/', data=trial, format='json')
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
