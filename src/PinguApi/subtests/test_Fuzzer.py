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
from PinguApi.submodels.Fuzzer import Fuzzer
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from unittest.mock import patch, MagicMock
from PinguApi.tasks import upload_fuzzer_to_bucket
class FuzzerTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.fuzzer_zip = open('PinguApi/subtests/test.zip', 'rb').read()
        self.test_Fuzzer = self.init_test_Fuzzer()
        

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Fuzzer(self):
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
            "stats_columns": "dasdas",
            "stats_column_descriptions": "dasd",
            "builtin": True,
            "differential": False,
            "has_large_testcases": False,
            "data_bundle_name": "dsadad",
            "fuzzer_zip": base64.b64encode(self.fuzzer_zip).decode('utf-8'),
        }
        Fuzzer_object = Fuzzer.objects.create(**fuzzer)
        Fuzzer_object.save()
        return Fuzzer_object
            
    @patch('PinguApi.tasks.upload_fuzzer_to_bucket.apply')
    def test_create_Fuzzers(self, mock_apply: MagicMock):
        fuzzer = {
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
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
            "stats_columns": "dasdas",
            "stats_column_descriptions": "dasd",
            "builtin": True,
            "differential": False,
            "has_large_testcases": False,
            "data_bundle_name": "dsadad",
            "fuzzer_zip": base64.b64encode(self.fuzzer_zip).decode('utf-8'),
        }
        
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/fuzzer/', data=fuzzer, format='json')
        
        # Assert that the Celery task was called with the correct arguments
        mock_apply.assert_called()
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Fuzzers(self):
        response = self.client.get(f'/api/fuzzer/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    @patch('PinguApi.tasks.download_fuzzer_from_bucket.apply')
    def test_get_Fuzzer(self, mock_apply: MagicMock):
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = self.fuzzer_zip
        mock_apply.return_value = mock_task
        
        response = self.client.get(f'/api/fuzzer/?id={self.test_Fuzzer.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    @patch('PinguApi.tasks.upload_fuzzer_to_bucket.apply')
    def test_update_Fuzzer(self, mock_apply: MagicMock):
        fuzzer_update = {
            "fuzzer_zip": base64.b64encode(self.fuzzer_zip).decode('utf-8'),
            "filename": "test_fuzzer.zip",
        }
        
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.patch(f'/api/fuzzer/{self.test_Fuzzer.id}/', data=fuzzer_update, format='json')
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