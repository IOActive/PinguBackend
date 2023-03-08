from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.TestCase import TestCase

class TestCaseTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_TestCase = self.init_test_TestCase()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_TestCase(self):
        testcase = {
            "bug_information": "",
            "test_case": b'',
            "fixed": False,
            "one_time_crasher_flag": False,
            "comments": "",
            "absolute_path": "fdsfsd",
            "queue": "tasks-linux",
            "archived": False,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "status": "pending",
            "triaged": False,
            "has_bug_flag": False,
            "open": False,
            "testcase_path": "fdsfsd",
            "additional_metadata": "",
            "fuzzed_keys": "",
            "minimized_keys": "",
            "minidump_keys": "",
            "minimized_arguments": "",
            "disable_ubsan": False,
            "regression": "",
            "timeout_multiplier": 1,
            "archive_state": 1,
            "redzone": 1
        }
        TestCase_object = TestCase.objects.create(**testcase)
        TestCase_object.save()
        return TestCase_object
            
    def test_create_TestCases(self):
        testcase = {
            "bug_information": "",
            "test_case": b'',
            "fixed": False,
            "one_time_crasher_flag": False,
            "comments": "",
            "absolute_path": "fdsfsd",
            "queue": "tasks-linux",
            "archived": False,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "status": "pending",
            "triaged": False,
            "has_bug_flag": False,
            "open": False,
            "testcase_path": "fdsfsd",
            "additional_metadata": "",
            "fuzzed_keys": "",
            "minimized_keys": "",
            "minidump_keys": "",
            "minimized_arguments": "",
            "disable_ubsan": False,
            "regression": "",
            "timeout_multiplier": 1,
            "archive_state": 1,
            "redzone": 1
        }
                
        response = self.client.put(f'/api/testcase/', data=testcase, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_TestCases(self):
        response = self.client.get(f'/api/testcase/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_TestCase(self):
        response = self.client.get(f'/api/testcase/?id={self.test_TestCase.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_TestCase(self):
        testcase_update = {
            "bug_information": "test"
        }
        
        response = self.client.patch(f'/api/testcase/{self.test_TestCase.id}/', data=testcase_update, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['bug_information'], "test")
