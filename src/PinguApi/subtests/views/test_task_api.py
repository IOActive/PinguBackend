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
from unittest.mock import MagicMock, patch
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from PinguApi.handlers.work_queue import create_queue, publish
from PinguApi.subtests.views.test_testcase_api import init_test_TestCase
from django.conf import settings
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_job_api import init_test_Job
from PinguApi.subtests.views.test_project_api import init_test_project

from PinguApi.submodels.task import Task
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.utilities.test_libs import helpers as test_helpers

class TaskTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)

        self.test_project = init_test_project()
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_job = init_test_Job(self.test_project)
        self.test_TestCase = init_test_TestCase(job=self.test_job, fuzzer=self.test_fuzzer)

        test_helpers.patch(self, [
            'PinguApi.handlers.work_queue.get_queue_element',
            'PinguApi.handlers.work_queue.queue_exists',
            'PinguApi.handlers.work_queue.publish',
            'PinguApi.handlers.work_queue.read_queue_elements',
        ])
        
        self.mock.get_queue_element.return_value = (False, {"message": "Task got added to queue"})
        self.mock.queue_exists.return_value = True
        self.mock.publish.return_value = True
        self.mock.read_queue_elements.return_value = (b'Bot Log', b'HeartBeat Log', b'Run Fuzzer Log', b'Run hearbeat Log')

    def test_add_libfuzz_task(self):
        task_test = {
            'job_id': str(self.test_job.id),
            'platform': 'Linux',
            'command': 'fuzz',
            'argument': 'libFuzzer',
        }
        
        response = self.client.post(f'/api/task/', data=task_test, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_blackbox_fuzz_task(self):
        task_test = {
            'job_id': str(self.test_job.id),
            'platform': 'Linux',
            'command': 'fuzz',
            'argument': 'blackFuzzer',
        }
        
        response = self.client.post(f'/api/task/', data=task_test, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_minimize_task(self):
        task_test = {
            'job_id': str(self.test_job.id),
            'platform': 'Linux',
            'command': 'minimize',
            'argument': str(self.test_TestCase.id),
        }
        
        response = self.client.post(f'/api/task/', data=task_test, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_task(self):
        response = self.client.get(f'/api/task/?platform=linux')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @patch('PinguApi.handlers.work_queue.read_queue_elements', MagicMock(return_value=(False,[])))
    def test_read_queue_tasks(self):
        response = self.client.get(f'/api/task/?read_queue')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
