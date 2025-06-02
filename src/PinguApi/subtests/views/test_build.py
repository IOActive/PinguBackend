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
from PinguApi.submodels.build import Build, Supported_Builds
from unittest.mock import patch, MagicMock

from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from django.core.files.uploadedfile import SimpleUploadedFile

def init_test_Build(build_zip, project):
    build = {
        "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "filename": "test_build",
        "file_size": "212",
        "blobstore_path": "builds/test.zip",
        #"build_zip": base64.b64encode(build_zip).decode('utf-8'),
        "type": Supported_Builds.RELEASE.value,
        "project": project
    }
    
    Build_object = Build.objects.create(**build)
    Build_object.save()
    return Build_object

class BuildTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.build_zip = open('src/PinguApi/subtests/views/test.zip', 'rb').read()
        self.test_project = init_test_project()
        self.test_Build = init_test_Build(self.build_zip, self.test_project)
         
    @patch('PinguApi.tasks.upload_build_to_bucket.delay')
    def test_create_build(self, mock_apply: MagicMock):
        build = {
            "filename": "test_build.zip",
            "type": Supported_Builds.RELEASE.value,
            "project_id": self.test_project.id,
            "build_zip": SimpleUploadedFile("test_build.zip", self.build_zip, content_type="application/zip")
        }
        
        # Mock the apply method of the upload_build_to_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.post(f'/api/build/', data=build, format='multipart')
    
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Builds(self):
        response = self.client.get(f'/api/build/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    @patch('PinguApi.tasks.download_build_from_bucket.apply')
    def test_get_build(self, mock_apply: MagicMock):
        
        # Mock the apply method of the download_build_from_bucket task
        mock_task = MagicMock()
        mock_task.get.return_value = self.build_zip
        mock_apply.return_value = mock_task
        
        response = self.client.get(f'/api/build/?id={self.test_Build.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    @patch('PinguApi.tasks.upload_build_to_bucket.delay')
    def test_update_build(self, mock_apply: MagicMock):
        build_update = {
            "filename": "test_build_updated.zip",
            "type": Supported_Builds.RELEASE.value,
            "build_zip": SimpleUploadedFile("test_build_updated.zip", self.build_zip, content_type="application/zip")
        }
        
        mock_task = MagicMock()
        mock_task.get.return_value = ('/path/to/blobstore', 12345)
        mock_apply.return_value = mock_task
        
        response = self.client.patch(f'/api/build/{self.test_Build.id}/', data=build_update, format='multipart')
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