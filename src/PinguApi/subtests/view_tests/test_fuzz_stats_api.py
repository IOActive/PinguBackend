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

import datetime
import json
from unittest.mock import MagicMock, patch
from rest_framework.authtoken.models import Token
from PinguApi.subtests.view_tests.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.view_tests.test_corpus_api import init_test_Job
from PinguApi.subtests.view_tests.test_project_api import init_test_project
from PinguApi.subtests.view_tests.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.view_tests.test_fuzz_target_api import init_test_FuzzTarget
from django.utils import timezone
from rest_framework import status
from PinguApi.subtests.handlers_tests.test_fuzzer_stats import init_get_objects_mock, init_listObjects_mock
from PinguApi.handlers.minio_manager import MinioManger
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.handlers.big_query import BigQueryHelper


class FuzzStatsTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
        self.test_job2 = init_test_Job(self.test_project)
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_FuzzTarget = init_test_FuzzTarget(self.test_project, fuzzer=self.test_fuzzer)
        
        self.today = datetime.datetime.now(timezone.get_current_timezone())
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.two_days_ago = self.today - datetime.timedelta(days=2)
        self.helper = BigQueryHelper()
        self.mock_objects = []
        init_listObjects_mock(self.mock_objects, self.test_project, self.test_FuzzTarget, self.test_job, self.yesterday, self.two_days_ago)
        self.mock_side_effects = []
        init_get_objects_mock(self.mock_side_effects)
        self.init_stats()
        return super().setUp()
    
    @patch.object(FuzzTarget.objects, 'get')
    @patch.object(MinioManger, 'listObjects')
    @patch.object(MinioManger, 'get_object')
    def init_stats(self, mock_get_object: MagicMock, mock_listObjects: MagicMock, mock_get: MagicMock):
        mock_listObjects.return_value = self.mock_objects
        mock_get_object.side_effect = self.mock_side_effects
        mock_get.return_value = self.test_FuzzTarget
        
        self.helper.update_stats_since_date(date=self.yesterday)
        
    def test_get_fuzz_stats(self):
        payload = {
        "fuzz_target": f"{self.test_FuzzTarget.id}",
        "start_date": "2025-01-27",
        "end_date": "2025-02-01",
        "group_by": "by-job",
        "interval": "1 day"
        }
        response = self.client.post(f'/api/fuzzer_stats/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
