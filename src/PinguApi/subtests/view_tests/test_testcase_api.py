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
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from PinguApi.submodels.testcase import TestCase
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_job_api import init_test_Job
from PinguApi.subtests.views.test_project_api import init_test_project


def init_test_TestCase(job, fuzzer):
        testcase = {
            "bug_information": "",
            "test_case": b'',
            "fixed": False,
            "one_time_crasher_flag": False,
            "comments": "",
            "absolute_path": "fdsfsd",
            "queue": "tasks-linux",
            "archived": False,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "status": "pending",
            "triaged": False,
            "has_bug_flag": False,
            "open": False,
            "testcase_path": "fdsfsd",
            "additional_metadata": "",
            "fuzzed_keys": "",
            "minimized_keys": "",
            "minidump_keys": "",
            "minimized_arguments": "",
            "disable_ubsan": False,
            "regression": "",
            "timeout_multiplier": 1,
            "archive_state": 1,
            "redzone": 1,
            "job": job,
            "fuzzer": fuzzer,
        }
        TestCase_object = TestCase.objects.create(**testcase)
        TestCase_object.save()
        return TestCase_object
    
class TestCaseTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_job = init_test_Job(self.test_project)
        self.test_TestCase = init_test_TestCase(job=self.test_job, fuzzer=self.test_fuzzer)

           
    def test_create_TestCases(self):
        testcase = {
            "bug_information": "",
            "test_case": b'',
            "fixed": "False",
            "one_time_crasher_flag": False,
            "comments": "",
            "absolute_path": "fdsfsd",
            "queue": "tasks-linux",
            "archived": False,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "status": "pending",
            "triaged": False,
            "has_bug_flag": False,
            "open": False,
            "testcase_path": "fdsfsd",
            "additional_metadata": "",
            "fuzzed_keys": "",
            "minimized_keys": "",
            "minidump_keys": "",
            "minimized_arguments": "",
            "disable_ubsan": False,
            "regression": "",
            "timeout_multiplier": 1,
            "archive_state": 1,
            "redzone": 1,
            "job_id": self.test_job.id,
            "fuzzer_id": self.test_fuzzer.id,
        }
                
        response = self.client.post(f'/api/testcase/', data=testcase, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_TestCases(self):
        response = self.client.get(f'/api/testcase/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_TestCase(self):
        response = self.client.get(f'/api/testcase/?id={self.test_TestCase.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_TestCase(self):
        testcase_update = {
            "bug_information": "test"
        }
        
        response = self.client.patch(f'/api/testcase/{self.test_TestCase.id}/', data=testcase_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['bug_information'], "test")
