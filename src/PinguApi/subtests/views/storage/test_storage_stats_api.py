from uuid import uuid4
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from unittest.mock import patch
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_project_api import init_test_project
from datetime import datetime

from PinguApi.subtests.views.test_job_api import init_test_Job

class StatsUploadViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        # Initialize test data
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        self.job = init_test_Job(self.project)      
          
        # Sample files for upload
        self.file1 = SimpleUploadedFile("stats1.json", b'{"data": "stats1"}', content_type="application/json")
        self.file2 = SimpleUploadedFile("stats2.json", b'{"data": "stats2"}', content_type="application/json")
        
        self.url = '/api/storage/stats/upload/'  # Adjust to match your URL pattern

    @patch('PinguApi.tasks.store_stats.delay')
    def test_successful_upload(self, mock_store_stats):
        # Test a successful stats upload
        # Mock the task result
        mock_store_stats.return_value.get.return_value = None  # Simulating successful task execution
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
            'job_id': str(self.job.id),
            'kind': 'TestCaseRun',  # Valid kind value
        }

        # Files should match the serializer field name 'files'
        files = {
            'files': [self.file1, self.file2],
        }
        
        data = {**data, **files}

        # Make the POST request
        response = self.client.post(
            self.url,
            data=data,
            format='multipart'
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'message': 'Stats uploaded'
        })
        
        # Check the mocked task call
        called_args = mock_store_stats.call_args
        bucket_name = "test-bigquery-bucket"  # Adjust based on your project configuration
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        expected_path = f"{self.fuzz_target.fuzzer.id}_{self.fuzz_target.binary}/{self.job.id}/TestCaseRun/{formatted_date}/"
        
        # Verify the task arguments
        self.assertEqual(called_args[0][0], bucket_name)  # bucket_name
        self.assertEqual(called_args[0][1], expected_path)  # storage_path
        uploaded_files = called_args[0][2]
        self.assertEqual(len(uploaded_files), 2)
        self.assertEqual(uploaded_files[0]['name'], "stats1.json")
        self.assertEqual(uploaded_files[1]['name'], "stats2.json")
        self.assertEqual(uploaded_files[0]['content_type'], "application/json")
        self.assertEqual(uploaded_files[1]['content_type'], "application/json")

    def test_project_not_found(self):
        # Test when project_id doesn’t exist
        data = {
            'project_id': str(uuid4()),
            'fuzz_target_id': str(self.fuzz_target.id),
            'job_id': str(self.job.id),
            'kind': 'TestCaseRun',
            'files': [self.file1]
        }
        
        response = self.client.post(self.url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Project does not exist.',
            'errors': {'detail': 'Project does not exist.'},
            'success': False
        })

    def test_fuzz_target_not_found(self):
        # Test when fuzz_target_id doesn’t exist or doesn’t match project
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(uuid4()),
            'job_id': str(self.job.id),
            'kind': 'TestCaseRun',
            'files': [self.file1]
        }
        
        response = self.client.post(self.url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Fuzz target does not exist.',
            'errors': {'detail': 'Fuzz target does not exist.'},
            'success': False
        })

    def test_job_not_found(self):
        # Test when job_id doesn’t exist
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
            'job_id': str(uuid4()),
            'kind': 'TestCaseRun',
            'files': [self.file1]
        }
        
        response = self.client.post(self.url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Job does not exists',
            'errors': {'detail': 'Job does not exists'},
            'success': False
        })

    def test_invalid_request_data(self):
        # Test with missing required fields (e.g., kind)
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
            'job_id': str(self.job.id),
            # 'kind' is missing
            'files': [self.file1]
        }
        
        response = self.client.post(self.url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'status': 400,
            'message': 'Invalid Request',
            'errors': {'detail': 'Invalid Request'},
            'success': False
        })

    @patch('PinguApi.tasks.store_stats.apply')
    def test_invalid_kind(self, mock_store_stats):
        # Test with an invalid 'kind' value
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
            'job_id': str(self.job.id),
            'kind': 'InvalidKind',  # Not TestCaseRun or JobRun
            'files': [self.file1]
        }
        
        response = self.client.post(self.url, data=data, format='multipart')
        
        # Assertions (assuming serializer validates kind)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'status': 400,
            'message': 'Invalid Request',
            'errors': {'detail': 'Invalid Request'},
            'success': False
        })