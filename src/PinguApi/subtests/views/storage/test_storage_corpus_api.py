from uuid import uuid4
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from unittest.mock import patch, MagicMock
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_project_api import init_test_project
import io
import zipfile

class CorpusDownloadViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        # Initialize test data
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        
        # URL for the download endpoint
        self.url = f'/api/storage/corpus/download/?project_id={self.project.id}&fuzz_target_id={self.fuzz_target.id}'

    @patch('PinguApi.tasks.download_corpus.apply')
    def test_successful_download(self, mock_task_apply):
        # Test a successful corpus download
        # Mock the download_corpus task result
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("testfile1.txt", "dummy content 1")
            zip_file.writestr("testfile2.txt", "dummy content 2")
        zip_stream.seek(0)
        
        mock_result = MagicMock()
        mock_result.get.return_value = zip_stream
        mock_task_apply.return_value = mock_result

        # Make the GET request
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.get('Content-Disposition'),
            f'attachment; filename="corpus_{self.project.name}_{self.fuzz_target.fuzzer.name}_{self.fuzz_target.binary}.zip"'
        )
        self.assertEqual(response.get('Content-Type'), 'application/zip')

        # Verify task was called with correct arguments
        expected_path = f"{self.fuzz_target.fuzzer.name}_{self.fuzz_target.binary}"
        mock_task_apply.assert_called_once_with(args=[
            'test-corpus-bucket',
            f"{self.fuzz_target.fuzzer.name}_{self.fuzz_target.binary}"
            ]
    )

        # Check ZIP contents
        # Check ZIP contents
        zip_bytes = b''.join(response.streaming_content)
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zip_ref:
            file_list = zip_ref.namelist()
            self.assertEqual(sorted(file_list), ["testfile1.txt", "testfile2.txt"])

    @patch('PinguApi.tasks.download_corpus.apply')
    def test_no_files_found(self, mock_task_apply):
        # Test when no corpus files are found (task returns None)
        mock_result = MagicMock()
        mock_result.get.return_value = None
        mock_task_apply.return_value = mock_result

        # Make the GET request
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'No corpus files found or failed to retrieve corpus.',
            'errors': {'detail': 'No corpus files found or failed to retrieve corpus.'},
            'success': False
        })

    def test_project_not_found(self):
        # Test when project_id doesn’t exist
        invalid_url = f'/api/storage/corpus/download/?project_id={uuid4()}&fuzz_target_id={self.fuzz_target.id}'
        response = self.client.get(invalid_url)

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
        invalid_url = f'/api/storage/corpus/download/?project_id={self.project.id}&fuzz_target_id={uuid4()}'
        response = self.client.get(invalid_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Fuzz target does not exist.',
            'errors': {'detail': 'Fuzz target does not exist.'},
            'success': False
        })

    def test_missing_parameters(self):
        # Test with missing required query parameters
        invalid_url = '/api/storage/corpus/download/'  # No project_id or fuzz_target_id
        response = self.client.get(invalid_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.json(), {
            'status': 406,
            'message': 'Missing project_id or fuzz_target_id',
            'errors': {'detail': 'Missing project_id or fuzz_target_id'},
            'success': False
        })

class CorpusUploadViewTest(PinguAPITestCase):
    def setUp(self):
        # Set up test client and sample data
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.fuzz_target = init_test_FuzzTarget(self.project, fuzzer=self.fuzzer)
        
        # Sample files for upload
        self.file1 = SimpleUploadedFile("testfile1.txt", b"dummy content 1", content_type="text/plain")
        self.file2 = SimpleUploadedFile("testfile2.txt", b"dummy content 2", content_type="text/plain")
        
        self.url = '/api/storage/corpus/upload/'  # Adjust to match your URL pattern

    @patch('PinguApi.tasks.store_corpus.delay')  # Mock Celery task
    def test_successful_upload(self, mock_store_corpus):
        # Test a successful corpu
        # s upload
        # Prepare the data
        data = {
            'project_id': str(self.project.id),
            'fuzz_target_id': str(self.fuzz_target.id),
        }

        # Files should match the serializer field name 'files'
        files = {
            'files': [self.file1, self.file2],  # Use 'files' to match CorpusUploadSerializer
        }
        
        data = {**data, **files}

        # Make the POST request
        response = self.client.post(
            self.url,
            data=data,
            format='multipart'  # Use format='multipart' instead of content_type
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'message': 'Corpus uploaded'
        })
        
        # Check the mocked task call
        called_args = mock_store_corpus.call_args
        expected_path = f"{self.fuzz_target.fuzzer.name}_{self.fuzz_target.binary}/"
        
        # Verify the storage path
        self.assertEqual(called_args[0][0], 'test-corpus-bucket')
        self.assertEqual(called_args[0][1], expected_path)
        
        # Verify the files (account for InMemoryUploadedFile transformation)
        uploaded_files = called_args[0][2]
        self.assertEqual(len(uploaded_files), 2)
        self.assertEqual(uploaded_files[0]['name'], "testfile1.txt")
        self.assertEqual(uploaded_files[1]['name'], "testfile2.txt")
        self.assertEqual(uploaded_files[0]['content_type'], "text/plain")
        self.assertEqual(uploaded_files[1]['content_type'], "text/plain")
        
    def test_project_not_found(self):
        # Test when project_id doesn’t exist
        data = {
            'project_id': uuid4(),
            'fuzz_target_id': uuid4(),
            'files': [self.file1]
        }
        
        # Make the POST request
        response = self.client.post(
            self.url,
            data=data,
            format='multipart'  # Use format='multipart' instead of content_type
        )
        
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
        files = [('files', self.file1)]
        
        response = self.client.post(self.url, data=data, files=files, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {
            'status': 404,
            'message': 'Fuzz target does not exist.',
            'errors': {'detail': 'Fuzz target does not exist.'},
            'success': False
        })

    def test_invalid_request_data(self):
        # Test with missing required fields
        data = {
            'project_id': 'proj123',
            # Missing fuzz_target_id
        }
        files = [('files', self.file1)]
        
        response = self.client.post(self.url, data=data, files=files, format='multipart')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'status': 400,
            'message': 'Invalid Request',
            'errors': {'detail': 'Invalid Request'},
            'success': False
        })