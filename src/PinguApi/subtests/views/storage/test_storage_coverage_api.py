from uuid import uuid4
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from unittest.mock import patch
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_project_api import init_test_project

class CoverageUploadViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        # Initialize test data
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        
        # Sample files for upload
        self.file1 = SimpleUploadedFile("coverage1.cov", b"coverage data 1", content_type="application/octet-stream")
        self.file2 = SimpleUploadedFile("coverage2.cov", b"coverage data 2", content_type="application/octet-stream")
        
        self.url = '/api/storage/coverage/upload/'  # Adjust to match your URL pattern

    @patch('PinguApi.utilities.configuration.get_value')
    @patch('PinguApi.tasks.store_coverage.delay')
    def test_successful_upload(self, mock_store_coverage, mock_get_value):
        # Test a successful coverage upload
        # Mock the configuration to return a bucket name
        mock_get_value.return_value = "test-coverage-bucket"
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
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
            'message': 'Stats uploaded'  # Note: View says "Stats uploaded", might want "Coverage uploaded"
        })
        
        # Check the mocked task call
        called_args = mock_store_coverage.call_args
        bucket_name = "test-coverage-bucket"
        expected_path = f"{self.fuzz_target.fuzzer.name}_{self.fuzz_target.binary}/"
        
        # Verify the task arguments
        self.assertEqual(called_args[0][0], bucket_name)  # bucket_name
        self.assertEqual(called_args[0][1], expected_path)  # storage_path
        uploaded_files = called_args[0][2]
        self.assertEqual(len(uploaded_files), 2)
        self.assertEqual(uploaded_files[0]['name'], "coverage1.cov")
        self.assertEqual(uploaded_files[1]['name'], "coverage2.cov")
        self.assertEqual(uploaded_files[0]['content_type'], "application/octet-stream")
        self.assertEqual(uploaded_files[1]['content_type'], "application/octet-stream")

    def test_project_not_found(self):
        # Test when project_id doesn’t exist
        data = {
            'project_id': str(uuid4()),
            'fuzz_target_id': str(self.fuzz_target.id),
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

    def test_invalid_request_data(self):
        # Test with missing required fields (e.g., fuzz_target_id)
        data = {
            'project_id': str(self.project.id),
            # 'fuzz_target_id' is missing
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

    @patch('PinguApi.utilities.configuration.get_value')
    def test_configuration_error(self, mock_get_value):
        # Test when bucket name retrieval fails
        mock_get_value.side_effect = Exception("Invalid configuration")
        
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
            'files': [self.file1]
        }
        
        response = self.client.post(self.url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {
            'status': 500,
            'message': 'Failed to get bucket name from configuration',
            'errors': {'detail': 'Failed to get bucket name from configuration'},
            'success': False
        })