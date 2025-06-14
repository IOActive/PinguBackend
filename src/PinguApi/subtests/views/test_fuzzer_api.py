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
from django.contrib.auth import get_user_model
from PinguApi.submodels.fuzzer import Fuzzer
import base64
from unittest.mock import patch, MagicMock
from PinguApi.tasks import upload_fuzzer_to_bucket
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from django.core.files.uploadedfile import SimpleUploadedFile

def init_test_Fuzzer(project):
        fuzzer_zip = open('src/PinguApi/subtests/views/test.zip', 'rb').read()
        stats_column_descriptions = '''fuzzer: "Fuzz target"
tests_executed: "Number of testcases executed during this time period"
new_crashes: "Number of new unique crashes observed during this time period"
edge_coverage: "Coverage for this fuzz target (number of edges/total)"
cov_report: "Link to coverage report"
corpus_size: "Size of the minimized corpus generated based on code coverage (number of testcases and total size on disk)"
avg_exec_per_sec: "Average number of testcases executed per second"
fuzzing_time_percent: "Percent of expected fuzzing time that is actually spent fuzzing."
new_tests_added: "New testcases added to the corpus during fuzzing based on code coverage"
new_features: "New coverage features based on new tests added to corpus."
regular_crash_percent: "Percent of fuzzing runs that had regular crashes (other than ooms, leaks, timeouts, startup and bad instrumentation crashes)"
oom_percent: "Percent of fuzzing runs that crashed on OOMs (should be 0)"
leak_percent: "Percent of fuzzing runs that crashed on memory leaks (should be 0)"
timeout_percent: "Percent of fuzzing runs that had testcases timeout (should be 0)"
startup_crash_percent: "Percent of fuzzing runs that crashed on startup (should be 0)"
avg_unwanted_log_lines: "Average number of unwanted log lines in fuzzing runs (should be 0)"
total_fuzzing_time_hrs: "Total time in hours for which the fuzzer(s) ran. Will be lower if fuzzer hits a crash frequently."
logs: "Link to fuzzing logs"
corpus_backup: "Backup copy of the minimized corpus generated based on code coverage"'''

        stats_columns = """sum(t.number_of_executed_units) as tests_executed,
    max(j.new_crashes) as new_crashes,
    _EDGE_COV as edge_coverage,
    _COV_REPORT as cov_report,
    _CORPUS_SIZE as corpus_size,
    avg(t.average_exec_per_sec) as avg_exec_per_sec,
    avg(t.fuzzing_time_percent) as fuzzing_time_percent,
    sum(t.new_units_added) as new_tests_added,
    sum(t.new_features) as new_features,
    avg(t.crash_count*100) as regular_crash_percent,
    avg(t.oom_count*100) as oom_percent,
    avg(t.leak_count*100) as leak_percent,
    avg(t.timeout_count*100) as timeout_percent,
    avg(t.startup_crash_count*100) as startup_crash_percent,
    avg(t.log_lines_unwanted) as avg_unwanted_log_lines,
    sum(t.actual_duration/3600.0) as total_fuzzing_time_hrs,
    _FUZZER_RUN_LOGS as logs,
    _CORPUS_BACKUP as corpus_backup,"""
        fuzzer = {
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "name": "test_fuzzer",
            "filename": "test_fuzzer",
            "file_size": "212",
            "blobstore_path": "fuzzers/test.zip",
            "executable_path": "adsad",
            "revision": 1.0,
            "timeout": 1,
            "supported_platforms": "dsada",
            "launcher_script": "dsada",
            "result": "dsada",
            "result_timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "console_output": "dsada",
            "return_code": 0,
            "sample_testcase": "dsadasd",
            "max_testcases": 3,
            "untrusted_content": False,
            "additional_environment_string": "dsadas",
            "stats_columns": stats_columns,
            "stats_column_descriptions": stats_column_descriptions,
            "builtin": True,
            "differential": False,
            "has_large_testcases": False,
            "data_bundle_name": "dsadad",
            #"fuzzer_zip": base64.b64encode(fuzzer_zip).decode('utf-8'),
            "project": project
        }
        Fuzzer_object = Fuzzer.objects.create(**fuzzer)
        Fuzzer_object.save()
        return Fuzzer_object, fuzzer_zip

class FuzzerTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_Fuzzer, self.fuzzer_zip = init_test_Fuzzer(self.test_project)
            
    @patch('PinguApi.tasks.upload_fuzzer_to_bucket.delay')
    def test_create_Fuzzers(self, mock_apply: MagicMock):
        fuzzer = {
            "name": "test_fuzzer2",
            "filename": "test_fuzzer32.zip",
            "file_size": "12",
            "blobstore_path": "sadsad",
            "executable_path": "adsad",
            "revision": 1.0,
            "timeout": 1,
            "supported_platforms": "Windows",
            "launcher_script": "dsada",
            "result": "dsada",
            "result_timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "console_output": "dsada",
            "return_code": 0,
            "sample_testcase": "dsadasd",
            "max_testcases": 3,
            "untrusted_content": False,
            "additional_environment_string": "dsadas",
            "stats_columns": '{"dasdas": "dasdas"}',
            "stats_column_descriptions": '{"dasd": "dasdas"}',
            "builtin": True,
            "differential": False,
            "has_large_testcases": False,
            "data_bundle_name": "dsadad",
            "fuzzer_zip": SimpleUploadedFile("test_fuzzer32.zip", self.fuzzer_zip, content_type="application/zip"),
            "project_id": self.test_project.id
        }
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/fuzzer/', data=fuzzer, format='multipart')
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Fuzzers(self):
        response = self.client.get(f'/api/fuzzer/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    @patch('PinguApi.tasks.download_fuzzer_from_bucket.apply')
    def test_get_Fuzzer(self, mock_apply: MagicMock):
        
        # Mock the apply method of the download_fuzzer_from_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = self.fuzzer_zip
        mock_apply.return_value = mock_task
        
        response = self.client.get(f'/api/fuzzer/?id={self.test_Fuzzer.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    @patch('PinguApi.tasks.upload_fuzzer_to_bucket.delay')
    def test_update_Fuzzer(self, mock_apply: MagicMock):
        fuzzer_update = {
            "fuzzer_zip": SimpleUploadedFile("test_fuzzer.zip", self.fuzzer_zip, content_type="application/zip"),
            "filename": "test_fuzzer.zip",
        }
        
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.patch(f'/api/fuzzer/{self.test_Fuzzer.id}/', data=fuzzer_update, format='multipart')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @patch('PinguApi.tasks.remove_fuzzer_from_bucket.apply')
    def test_remove_fuzzer(self, mock_apply):
        mock_task = MagicMock()
        mock_task.get.return_value = None
        mock_apply.return_value = mock_task
        
        response = self.client.delete(f'/api/fuzzer/{self.test_Fuzzer.id}/')
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)