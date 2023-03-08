from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.Fuzzer import Fuzzer

class FuzzerTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Fuzzer = self.init_test_Fuzzer()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Fuzzer(self):
        fuzzer = {
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "name": "test_fuzzer",
            "filename": "test_fuzzer",
            "file_size": "12",
            "blobstore_path": "sadsad",
            "executable_path": "adsad",
            "revision": 1.0,
            "timeout": 1,
            "supported_platforms": "dsada",
            "launcher_script": "dsada",
            "result": "dsada",
            "result_timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "console_output": "dsada",
            "return_code": 0,
            "sample_testcase": "dsadasd",
            "max_testcases": 3,
            "untrusted_content": False,
            "additional_environment_string": "dsadas",
            "stats_columns": "dasdas",
            "stats_column_descriptions": "dasd",
            "builtin": True,
            "differential": False,
            "has_large_testcases": False,
            "data_bundle_name": "dsadad"
        }
        Fuzzer_object = Fuzzer.objects.create(**fuzzer)
        Fuzzer_object.save()
        return Fuzzer_object
            
    def test_create_Fuzzers(self):
        fuzzer = {
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "name": "test_fuzzer2",
            "filename": "test_fuzzer",
            "file_size": "12",
            "blobstore_path": "sadsad",
            "executable_path": "adsad",
            "revision": 1.0,
            "timeout": 1,
            "supported_platforms": "dsada",
            "launcher_script": "dsada",
            "result": "dsada",
            "result_timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "console_output": "dsada",
            "return_code": 0,
            "sample_testcase": "dsadasd",
            "max_testcases": 3,
            "untrusted_content": False,
            "additional_environment_string": "dsadas",
            "stats_columns": "dasdas",
            "stats_column_descriptions": "dasd",
            "builtin": True,
            "differential": False,
            "has_large_testcases": False,
            "data_bundle_name": "dsadad"
        }
        
        response = self.client.put(f'/api/fuzzer/', data=fuzzer, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Fuzzers(self):
        response = self.client.get(f'/api/fuzzer/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_Fuzzer(self):
        response = self.client.get(f'/api/fuzzer/?id={self.test_Fuzzer.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_Fuzzer(self):
        fuzzer_update = {
            "file_size": "13MB",
        }
        
        response = self.client.patch(f'/api/fuzzer/{self.test_Fuzzer.id}/', data=fuzzer_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['file_size'], "13MB")
