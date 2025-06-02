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

import base64
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.authtoken.models import Token
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_job_api import init_test_Job
from PinguApi.subtests.views.test_project_api import init_test_project

from django.conf import settings

from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_testcase_api import init_test_TestCase
from third_party.django.core.files.uploadedfile import SimpleUploadedFile

class CustomBinaryTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        self.test_project = init_test_project()
        self.test_fuzzer, self.fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_job = init_test_Job(self.test_project)
        self.test_testCase = init_test_TestCase(job=self.test_job, fuzzer=self.test_fuzzer)
        self.custom_binary_zip = open('src/PinguApi/subtests/views/test.zip', 'rb').read()


      
    @patch('PinguApi.tasks.upload_custom_binary_to_bucket.delay')
    def test_add_custom_binary_to_job(self, mock_apply: MagicMock):
        custom_binary_payload = {
            'job_id': self.test_job.id,
            "custom_binary": SimpleUploadedFile(
                "test_custom_binary.zip",
                self.custom_binary_zip,
                content_type="application/zip"),
            'file_name': 'test.zip',
        }
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/custom_binary/', data=custom_binary_payload, format='multipart')
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    @patch('PinguApi.tasks.remove_custom_binary_from_bucket.delay')
    def test_delete_custom_binary_to_job(self, mock_apply: MagicMock):
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = (True)
        mock_apply.return_value = mock_task
        
        response = self.client.delete(f'/api/custom_binary/?job_id={self.test_job.id}')
            
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)