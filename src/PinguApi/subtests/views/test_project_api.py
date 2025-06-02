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
from unittest.mock import MagicMock, patch
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from PinguApi.models import Project
from rest_framework import status
from PinguApi.storage_providers.storage_provider import StorageProvider
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from minio.helpers import ObjectWriteResult
import yaml


def init_test_project():
    default_configuration = open("default_yml_configs/deafult_project_config.yaml", "r").read()
    
    project = {
        "name": "super-project",
        "description": "super project",
        "configuration": yaml.safe_load(default_configuration)
    }
    project_o = Project.objects.create(**project)
    project_o.save()
    return project_o

class ProjectTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.project_o = init_test_project()
    
    @patch.object(StorageProvider, 'create_bucket')
    def test_register(self,  mock_create_bucket):
        
        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result = None
        # Set the return value of the mock_put_object method
        mock_create_bucket.return_value = mock_result
        
        project = {
            "name": "super-project2",
            "description": "super project 2"
        }
        
        response = self.client.post(f'/api/project/', data=project, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get(self):
        response = self.client.get(f'/api/project/?id={self.project_o.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @patch('PinguApi.subviews.project_view.Project_Update_Delete_APIView.post_delete_task')
    def test_delete(self, post_delete_task_mock: MagicMock):
        post_delete_task_mock.return_value = None
        response = self.client.delete(f'/api/project/{self.project_o.id}/')
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_patch(self):
        test_project_config_yml = open("default_yml_configs/deafult_project_config.yaml").read()
        project_config = {'configuration': test_project_config_yml,
               }
        response = self.client.patch(f'/api/project/{self.project_o.id}/', 
                                     data=project_config, format='json')
        
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)