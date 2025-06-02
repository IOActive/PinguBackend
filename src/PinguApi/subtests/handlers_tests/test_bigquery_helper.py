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
from src.PinguApi.handlers.big_query import BigQueryHelper
from unittest.mock import MagicMock, ANY, patch
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_job_api import init_test_Job
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from rest_framework.authtoken.models import Token
from minio.datatypes import Object
import os
from django.utils import timezone
from minio.helpers import ObjectWriteResult
from PinguApi.storage_providers.storage_provider import StorageProvider
from PinguApi.submodels.fuzz_target import FuzzTarget

class TestBigQueryHelper(PinguAPITestCase):
        
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_FuzzTarget = init_test_FuzzTarget(self.test_project, fuzzer=self.test_fuzzer)
        
        self.today = datetime.datetime.now(timezone.get_current_timezone())
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.two_days_ago = self.today - datetime.timedelta(days=2)
        self.helper = BigQueryHelper()
        self.init_listObjects_mock()
        self.init_get_objects_mock()
        return super().setUp()
    
    def get_all_file_paths(self, folder_path: str):
        """Return a list of all file paths in the given folder and subfolders."""
        file_paths = []
        
        # Walk through directory and subdirectories
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        
        return file_paths

    def init_get_objects_mock(self):
        """Initialize the mock objects for get_object."""
        # Create a mocked ObjectWriteResult object
        
        self.mock_side_effects = []
        for file in self.get_all_file_paths('src/PinguApi/subtests/test_data/stats'):
            with open(file, 'rb') as f:
                # Read the file content and append it to the list of side effects
                mock_result = MagicMock(spec=ObjectWriteResult)
                mock_result.data = f.read()
                self.mock_side_effects.append(mock_result)
        

    def init_listObjects_mock(self):
        paths = self.get_all_file_paths("src/PinguApi/subtests/test_data/stats/")
        self.mock_objects = []

        for path in paths:
            clean_path = path.split('stats/')[1]
            full_path = f"{self.test_project.id}/{self.test_FuzzTarget.fuzzer.id}_{self.test_FuzzTarget.binary}/{self.test_job.id}/{clean_path}"
            mock_object = Object(
                bucket_name="test-bigquery-buket",
                object_name=full_path,
                last_modified=self.yesterday
            )
            self.mock_objects.append(mock_object)
        
        # ADD mock object from 2 day ago
        self.mock_object_old = Object(
            bucket_name="test-bigquery-buket",
            object_name=f"{self.test_project.id}/{self.test_FuzzTarget.fuzzer.id}_{self.test_FuzzTarget.binary}/{self.test_job.id}/stats/2dayago.json",
            last_modified=self.two_days_ago
            )
        self.mock_objects.append(self.mock_object_old)
        
    @patch.object(StorageProvider, 'list_blobs')
    def test_get_project_stats(self, mock_listObjects: MagicMock):
        mock_listObjects.return_value = self.mock_objects
        self.helper.monitor_project_stats_since_date(date=self.yesterday)
        
        # assert that the old object is not monitored as it is from 2 days ago and only yesterday's data should be monitored
        assert(self.mock_object_old not in self.helper.monitored_objects)
    
    @patch.object(FuzzTarget.objects, 'get')
    @patch.object(StorageProvider, 'list_blobs')
    @patch.object(StorageProvider, 'get')
    def test_update_new_stats(self, mock_get_object: MagicMock, mock_listObjects: MagicMock, mock_get: MagicMock):
        mock_listObjects.return_value = self.mock_objects
        mock_get_object.side_effect = self.mock_side_effects
        mock_get.return_value = self.test_FuzzTarget
        
        self.helper.update_stats_since_date(date=self.yesterday)