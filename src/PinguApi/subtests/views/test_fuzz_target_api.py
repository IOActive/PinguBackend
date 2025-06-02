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

from rest_framework.test import force_authenticate
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer

        
def init_test_FuzzTarget(project, fuzzer):
    fuzztarget = {
        "project": project,
        "binary": "sadad",
        "fuzzer": fuzzer
    }
    FuzzTarget_object = FuzzTarget.objects.create(**fuzztarget)
    FuzzTarget_object.save()
    return FuzzTarget_object
class FuzzTargetTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_FuzzTarget = init_test_FuzzTarget(self.test_project, fuzzer=self.test_fuzzer)

            
    def test_create_FuzzTargets(self):
        fuzztarget = {
            "project_id": self.test_project.id,
            "binary": "sadad",
            "fuzzer_id": self.test_fuzzer.id
        }
        
        response = self.client.post(f'/api/fuzztarget/', data=fuzztarget, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_FuzzTargets(self):
        response = self.client.get(f'/api/fuzztarget/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_FuzzTarget(self):
        response = self.client.get(f'/api/fuzztarget/?id={self.test_FuzzTarget.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_FuzzTarget(self):
        fuzztarget_update = {
            "binary": "test_project2",
        }
        
        response = self.client.patch(f'/api/fuzztarget/{self.test_FuzzTarget.id}/', data=fuzztarget_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['binary'], "test_project2")
