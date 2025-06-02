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

from PinguApi.submodels.fuzz_target_job import FuzzTargetJob
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_job_api import init_test_Job


def init_test_FuzzTargetJob(fuzzer, fuzz_target, job):
    fuzztargetjob = {
        "weight": 1,
        "last_run": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "fuzzer": fuzzer,
        "fuzz_target": fuzz_target,
        "job": job
    }
    FuzzTargetJob_object = FuzzTargetJob.objects.create(**fuzztargetjob)
    FuzzTargetJob_object.save()
    return FuzzTargetJob_object
class FuzzTargetJobTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_FuzzTarget = init_test_FuzzTarget(self.test_project, fuzzer=self.test_fuzzer)
        self.test_FuzzTargetJob = init_test_FuzzTargetJob(fuzzer=self.test_fuzzer, fuzz_target=self.test_FuzzTarget, job=self.test_job)
        

            
    def test_create_FuzzTargetJobs(self):
        fuzztargetjob = {
            "weight": 1,
            "last_run": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "fuzzer_id": self.test_fuzzer.id,
            "fuzz_target_id": self.test_FuzzTarget.id,
            "job_id": self.test_job.id
        }
            
        response = self.client.post(f'/api/fuzztargetjob/', data=fuzztargetjob, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_FuzzTargetJobs(self):
        response = self.client.get(f'/api/fuzztargetjob/?job={self.test_job.id}')
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
