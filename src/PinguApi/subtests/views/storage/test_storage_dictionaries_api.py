import io
from uuid import uuid4
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from unittest.mock import patch, MagicMock
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_project_api import init_test_project

class DictionaryUploadViewTest(PinguAPITestCase):
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
        self.dictionary_file = SimpleUploadedFile("dictionary.dic", b"dictionary data", content_type="application/octet-stream")
        
        self.upload_url = '/api/storage/dictionaries/upload/'  # Adjust to match your URL pattern

    @patch('PinguApi.utilities.configuration.get_value')
    @patch('PinguApi.tasks.upload_dictionary.delay')
    def test_successful_upload(self, mock_upload_dictionary, mock_get_value):
        # Test a successful dictionary upload
        # Mock the configuration to return a bucket name
        mock_get_value.return_value = "test-dictionaries-bucket"
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary': self.dictionary_file
        }

        # Make the POST request
        response = self.client.post(
            self.upload_url,
            data=data,
            format='multipart'
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'status': 'success'
        })
        
        # Check the mocked task call
        called_args = mock_upload_dictionary.call_args
        bucket_name = "test-dictionaries-bucket"
        expected_path = f"{self.fuzz_target.fuzzer.name}_{self.fuzz_target.binary}"
        
        # Verify the task arguments
        self.assertEqual(called_args[0][0], bucket_name)  # bucket_name
        self.assertEqual(called_args[0][1], expected_path)  # storage_path
        uploaded_file = called_args[0][2]
        self.assertEqual(uploaded_file['name'], "dictionary.dic")
        self.assertEqual(uploaded_file['content_type'], "application/octet-stream")

    def test_project_not_found(self):
        # Test when project_id doesn’t exist
        data = {
            'project_id': str(uuid4()),
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary': self.dictionary_file
        }
        
        response = self.client.post(self.upload_url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Project does not exist.',
            'errors': {'detail': 'Project does not exist.'},
            'success': False
        })

    def test_fuzz_target_not_found(self):
        # Test when fuzztarget_id doesn’t exist or doesn’t match project
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(uuid4()),
            'dictionary': self.dictionary_file
        }
        
        response = self.client.post(self.upload_url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Fuzztarget does not exist.',
            'errors': {'detail': 'Fuzztarget does not exist.'},
            'success': False
        })

    def test_invalid_request_data(self):
        # Test with missing required fields (e.g., fuzztarget_id)
        data = {
            'project_id': str(self.project.id),
            # 'fuzztarget_id' is missing
            'dictionary': self.dictionary_file
        }
        
        response = self.client.post(self.upload_url, data=data, format='multipart')
        
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
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary': self.dictionary_file
        }
        
        response = self.client.post(self.upload_url, data=data, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {
            'status': 500,
            'message': 'Failed to get bucket name from configuration',
            'errors': {'detail': 'Failed to get bucket name from configuration'},
            'success': False
        })

class DictionaryDownloadViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        # Initialize test data
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        
        self.download_url = '/api/storage/dictionaries/download/'  # Adjust to match your URL pattern

    @patch('PinguApi.utilities.configuration.get_value')
    @patch('PinguApi.tasks.download_dictionary.apply')
    def test_successful_download(self, mock_download_dictionary, mock_get_value):
        # Mock the configuration to return a bucket name
        mock_get_value.return_value = "test-dictionaries-bucket"
        
        # Mock the download task to return a file stream
        mock_result = MagicMock()
        mock_result.get.return_value = io.BytesIO(b"dictionary data")
        mock_download_dictionary.return_value = mock_result
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary_name': 'dictionary.dic'
        }

        # Make the GET request
        response = self.client.get(self.download_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="dictionary.dic"')
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
    
        response_content = b''.join(response.streaming_content)
        self.assertEqual(response_content, b"dictionary data")

    def test_project_not_found(self):
        # Test when project_id doesn’t exist
        data = {
            'project_id': str(uuid4()),
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary_name': 'dictionary.dic'
        }
        
        response = self.client.get(self.download_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Project does not exist.',
            'errors': {'detail': 'Project does not exist.'},
            'success': False
        })

    def test_fuzz_target_not_found(self):
        # Test when fuzztarget_id doesn’t exist or doesn’t match project
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(uuid4()),
            'dictionary_name': 'dictionary.dic'
        }
        
        response = self.client.get(self.download_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Fuzztarget does not exist.',
            'errors': {'detail': 'Fuzztarget does not exist.'},
            'success': False
        })

    def test_invalid_request_data(self):
        # Test with missing required fields (e.g., dictionary_name)
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(self.fuzz_target.id),
            # 'dictionary_name' is missing
        }
        
        response = self.client.get(self.download_url, data=data)
        
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
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary_name': 'dictionary.dic'
        }
        
        response = self.client.get(self.download_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {
            'status': 500,
            'message': 'Failed to get bucket name from configuration',
            'errors': {'detail': 'Failed to get bucket name from configuration'},
            'success': False
        })

class DictionaryExistsViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        # Initialize test data
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        
        self.exists_url = '/api/storage/dictionaries/exists/'  # Adjust to match your URL pattern

    @patch('PinguApi.utilities.configuration.get_value')
    @patch('PinguApi.tasks.dictionary_exists.apply')
    def test_dictionary_exists(self, mock_dictionary_exists, mock_get_value):
        # Mock the configuration to return a bucket name
        mock_get_value.return_value = "test-dictionaries-bucket"
        
        # Mock the dictionary exists task to return True
        mock_result = MagicMock()
        mock_result.get.return_value = True
        mock_dictionary_exists.return_value = mock_result
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary_name': 'dictionary.dic'
        }

        # Make the GET request
        response = self.client.get(self.exists_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'status': 'exists'
        })

    @patch('PinguApi.utilities.configuration.get_value')
    @patch('PinguApi.tasks.dictionary_exists.apply')
    def test_dictionary_not_exists(self, mock_dictionary_exists, mock_get_value):
        # Mock the configuration to return a bucket name
        mock_get_value.return_value = "test-dictionaries-bucket"
        
        # Mock the dictionary exists task to return False
        mock_result = MagicMock()
        mock_result.get.return_value = False
        mock_dictionary_exists.return_value = mock_result
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(self.fuzz_target.id),
            'dictionary_name': 'dictionary.dic'
        }

        # Make the GET request
        response = self.client.get(self.exists_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 'not found'
        })

class ListDictionariesViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        # Initialize test data
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        
        self.list_url = '/api/storage/dictionaries/list/'  # Adjust to match your URL pattern

    @patch('PinguApi.utilities.configuration.get_value')
    @patch('PinguApi.tasks.list_dictionaries.apply')
    def test_list_dictionaries(self, mock_list_dictionaries, mock_get_value):
        # Mock the configuration to return a bucket name
        mock_get_value.return_value = "test-dictionaries-bucket"
        
        # Mock the list dictionaries task to return a list of dictionaries
        mock_result = MagicMock()
        mock_result.get.return_value = ["dictionary1.dic", "dictionary2.dic"]
        mock_list_dictionaries.return_value = mock_result
        
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzztarget_id': str(self.fuzz_target.id)
        }

        # Make the GET request
        response = self.client.get(self.list_url, data=data)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'dictionaries': ["dictionary1.dic", "dictionary2.dic"]
        })
