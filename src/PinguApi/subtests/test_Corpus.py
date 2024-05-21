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
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.subtests.test_Job import JobTests
from PinguApi.subtests.test_TestCase import TestCaseTests
from django.conf import settings
from PinguApi.subtests.test_Fuzzer import FuzzerTests

class CorpusTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.fuzzer_zip = open('PinguApi/subtests/test.zip', 'rb').read()
        self.test_job = JobTests.init_test_Job(self)
        self.test_fuzzer = FuzzerTests.init_test_Fuzzer(self)
        self.test_tesetcase = TestCaseTests.init_test_TestCase(self)
        self.custom_binary_zip = open('PinguApi/subtests/test.zip', 'rb').read()
        os.environ['CORPUS_BUCKET'] = 'test-corpus-bucket'
        

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    @patch('PinguApi.tasks.upload_corpus_to_bucket.apply')
    def test_add_corpus_to_job(self, mock_apply: MagicMock):
        corpus_payload = {
            'job_id': self.test_job.id,
            'corpus_binary': base64.b64encode(self.custom_binary_zip).decode('utf-8'),
            'filename': 'test.zip',
            'engine_id': self.test_fuzzer.id,
            'fuzztarget_name': 'test_fuzzTarget',
        }
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/corpus/', data=corpus_payload, format='json')
        
        # Assert that the Celery task was called with the correct arguments
        mock_apply.assert_called()
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        