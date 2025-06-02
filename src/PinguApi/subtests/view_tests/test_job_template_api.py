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
from rest_framework import status
from rest_framework.authtoken.models import Token

from PinguApi.submodels.Job_template import JobTemplate
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase

def init_test_JobTemplate():
    jobtemplate = {
        "name": "test_jobtemplate",
        "environment_string": ""
    }
    JobTemplate_object = JobTemplate.objects.create(**jobtemplate)
    JobTemplate_object.save()
    return JobTemplate_object
class JobTemplateTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_JobTemplate = init_test_JobTemplate()
            
    def test_create_JobTemplates(self):
        jobtemplate = {
            "name": "test_jobtemplate2",
            "environment_string": ""
        }
                
        response = self.client.post(f'/api/jobtemplate/', data=jobtemplate, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_JobTemplates(self):
        response = self.client.get(f'/api/jobtemplate/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_JobTemplate(self):
        response = self.client.get(f'/api/jobtemplate/?id={self.test_JobTemplate.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_JobTemplate(self):
        jobtemplate_update = {
            "name": "test_jobtemplate3",
        }
        
        response = self.client.patch(f'/api/jobtemplate/{self.test_JobTemplate.id}/', data=jobtemplate_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['name'], "test_jobtemplate3")
