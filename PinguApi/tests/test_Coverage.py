from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PinguApi.submodels.Coverage import Coverage

class CoverageTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        self.test_Coverage = self.init_test_Coverage()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        
    def init_test_Coverage(self):
        coverage = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "fuzzer": "test_fuzzer",
            "functions_covered": 1,
            "functions_total": 1,
            "edges_covered": 1,
            "edges_total": 1,
            "corpus_size_units": 1,
            "corpus_size_bytes": 1,
            "corpus_location": "/world/",
            "corpus_backup_location": "/world/",
            "quarantine_size_units": 1,
            "quarantine_size_bytes": 1,
            "quarantine_location": "/world/"
        }
        
        Coverage_object = Coverage.objects.create(**coverage)
        Coverage_object.save()
        return Coverage_object
            
    def test_create_Coverages(self):
        coverage = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "fuzzer": "test_fuzzer",
            "functions_covered": 1,
            "functions_total": 1,
            "edges_covered": 1,
            "edges_total": 1,
            "corpus_size_units": 1,
            "corpus_size_bytes": 1,
            "corpus_location": "/world/",
            "corpus_backup_location": "/world/",
            "quarantine_size_units": 1,
            "quarantine_size_bytes": 1,
            "quarantine_location": "/world/"
        }
        
        response = self.client.put(f'/api/coverage/', data=coverage, format='json')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_Coverages(self):
        response = self.client.get(f'/api/coverage/')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)

    def test_get_Coverage(self):
        response = self.client.get(f'/api/coverage/?id={self.test_Coverage.id}')
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(result) > 0)
        
    def test_update_Coverage(self):
        coverage_update = {
            "revision": 2,
        }
        
        response = self.client.patch(f'/api/coverage/{self.test_Coverage.id}/', json=coverage_update, format=json)
        result = json.loads(response.content)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['revision'], 2)
