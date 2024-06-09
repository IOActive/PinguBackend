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
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from PinguApi.submodels.Build import Build, Supported_Builds
import base64
from unittest.mock import patch, MagicMock

class BuildTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.build_zip = open('PinguApi/subtests/test.zip', 'rb').read()
        self.test_Build = self.init_test_Build()
        

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Build(self):
        build = {
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "filename": "test_build",
            "file_size": "212",
            "blobstore_path": "builds/test.zip",
            "build_zip": base64.b64encode(self.build_zip).decode('utf-8'),
            "type": Supported_Builds.RELEASE.value,
        }
        Build_object = Build.objects.create(**build)
        Build_object.save()
        return Build_object
            
    @patch('PinguApi.tasks.upload_build_to_bucket.apply')
    def test_create_build(self, mock_apply: MagicMock):
        build = {
            "filename": "test_build",
            "build_zip": base64.b64encode(self.build_zip).decode('utf-8'),
            "type": Supported_Builds.RELEASE.value,
        }
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/build/', data=build, format='json')
        
        # Assert that the Celery task was called with the correct arguments
        mock_apply.assert_called()
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Builds(self):
        response = self.client.get(f'/api/build/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    @patch('PinguApi.tasks.download_build_from_bucket.apply')
    def test_get_build(self, mock_apply: MagicMock):
        
        # Mock the apply method of the upload_fuzzer_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = self.build_zip
        mock_apply.return_value = mock_task
        
        response = self.client.get(f'/api/build/?id={self.test_Build.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    @patch('PinguApi.tasks.upload_build_to_bucket.apply')
    def test_update_build(self, mock_apply: MagicMock):
        fuzzer_update = {
            "build_zip": base64.b64encode(self.build_zip).decode('utf-8'),
            "filename": "test_build.zip",
            "type": Supported_Builds.RELEASE.value
        }
        
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.patch(f'/api/build/{self.test_Build.id}/', data=fuzzer_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @patch('PinguApi.tasks.remove_build_from_bucket.apply')
    def test_remove_build(self, mock_apply):
        mock_task = MagicMock()
        mock_task.get.return_value = None
        mock_apply.return_value = mock_task
        
        response = self.client.delete(f'/api/build/{self.test_Build.id}/')
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)