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
from uuid import uuid4
from rest_framework import status
from rest_framework.authtoken.models import Token

from PinguApi.submodels.crash_stats import CrashStats
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase

def init_test_stats():
        stats = {
            "crash_type": "Overflow",
            "crash_state": "Unknown",
            "platform": "Linux",
            "crash_time_in_ms": 100,
            "fuzzer": uuid4(),
            "testcase": uuid4(),
            "project": uuid4(),
            "job": uuid4(),
            "crash": uuid4(),
            "security_flag": True,
            "reproducible_flag": True,
            "revision": 1,
            "new_flag": True,
        }
        stats_object = CrashStats.objects.create(**stats)
        stats_object.save()
        return stats_object
    
class CrashStatsTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Trial = init_test_stats()

    def test_create_crash_stats(self):
        stats = {
            "crash_type": "Overflow",
            "crash_state": "Unknown",
            "platform": "Linux",
            "crash_time_in_ms": 100,
            "fuzzer_id": uuid4(),
            "testcase_id": uuid4(),
            "project_id": uuid4(),
            "job_id": uuid4(),
            "crash_id": uuid4(),
            "security_flag": True,
            "reproducible_flag": True,
            "revision": 1,
            "new_flag": True,
        }
        
        response = self.client.post(f'/api/crash_stats/', data=stats, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)