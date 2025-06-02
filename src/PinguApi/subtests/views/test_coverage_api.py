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
from PinguApi.submodels.coverage import Coverage
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_corpus_api import init_test_Job
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_testcase_api import init_test_TestCase
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase

class CoverageTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_project = init_test_project()
        self.test_fuzzer, self.fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_job = init_test_Job(self.test_project)
        self.test_TestCase = init_test_TestCase(job=self.test_job, fuzzer=self.test_fuzzer)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
            