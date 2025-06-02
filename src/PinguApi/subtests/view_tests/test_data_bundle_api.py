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
from PinguApi.submodels.data_bundle import DataBundle
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase


def init_test_DataBundle():
        databundle = {
            "name": "test_databundle",
            "bucket_name": "adsad",
            "source": "dasda",
            "is_local": False,
            "timestamp": "2023-03-07",
            "sync_to_worker": True
        }
        DataBundle_object = DataBundle.objects.create(**databundle)
        DataBundle_object.save()
        return DataBundle_object
class DataBundleTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_DataBundle = init_test_DataBundle()
       
    def test_create_DataBundles(self):
        databundle = {
            "name": "test_databundle",
            "bucket_name": "adsad",
            "source": "dasda",
            "is_local": False,
            "timestamp": "2023-03-07",
            "sync_to_worker": True
        }
        
        response = self.client.post(f'/api/databundle/', data=databundle, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_DataBundles(self):
        response = self.client.get(f'/api/databundle/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_DataBundle(self):
        response = self.client.get(f'/api/databundle/?id={self.test_DataBundle.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_DataBundle(self):
        databundle_update = {
            "is_local": True,
        }
        
        response = self.client.patch(f'/api/databundle/{self.test_DataBundle.id}/', data=databundle_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['is_local'], True)
