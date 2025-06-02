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
from PinguApi.submodels.statistic import Statistic
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_job_api import init_test_Job

def init_test_Statistic(job):
    statistic = {
        "iteration": 1,
        "runtime": 1,
        "execs_per_sec": 1,
        "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "last_beat_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "status": "started",
        "task_payload": "aa",
        "job": job
    }
    Statistic_object = Statistic.objects.create(**statistic)
    Statistic_object.save()
    return Statistic_object
class StatisticTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
        self.test_Statistic = init_test_Statistic(self.test_job)

            
    def test_create_Statistics(self):
        statistic = {
            "iteration": 1,
            "runtime": 1,
            "execs_per_sec": 1,
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "last_beat_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "status": "started",
            "task_payload": "aa",
            "job_id": self.test_job.id
        }
                
        response = self.client.post(f'/api/stadistics/', data=statistic, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Statistics(self):
        response = self.client.get(f'/api/stadistics/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_Statistic(self):
        response = self.client.get(f'/api/stadistics/?id={self.test_Statistic.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_Statistic(self):
        statistic_update = {
            "iteration": 2,
        }
        
        response = self.client.patch(f'/api/stadistics/{self.test_Statistic.id}/', data=statistic_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['iteration'], 2)
