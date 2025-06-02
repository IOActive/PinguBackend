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
from datetime import datetime
import os
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.authtoken.models import Token
from PinguApi.subtests.views.test_job_api import init_test_Job
from django.conf import settings
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_project_api import init_test_project
from django.core.files.uploadedfile import SimpleUploadedFile

from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget

class CorpusTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
        self.test_fuzzer, self.fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.fuzzer_target = init_test_FuzzTarget(project=self.test_project, fuzzer=self.test_fuzzer)
        
        self.custom_binary_zip = self.fuzzer_zip
        os.environ['CORPUS_BUCKET'] = 'test-corpus-bucket'
               
    @patch('PinguApi.tasks.upload_corpus_to_bucket.delay')
    def test_add_corpus_to_job(self, mock_apply: MagicMock):
        corpus_payload = {
            'job_id': self.test_job.id,
            'filename': 'test.zip',
            'fuzzer_id': self.test_fuzzer.id,
            'fuzztarget_name': self.fuzzer_target.binary,
            'corpus_binary': SimpleUploadedFile("test.zip", self.custom_binary_zip, content_type="application/zip")
        }
        
        # Mock the apply method of the upload_corpus_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/corpus/', data=corpus_payload, format='multipart')
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
