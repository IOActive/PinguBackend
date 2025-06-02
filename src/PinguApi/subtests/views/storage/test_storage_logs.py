import zipfile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from unittest.mock import MagicMock, patch
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_project_api import init_test_project
import io
from PinguApi.subtests.views.test_job_api import init_test_Job

class UploadLogsViewTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.job = init_test_Job(self.project)
        
        self.upload_url = '/api/storage/logs/upload/'
        
        self.bot_log_data = {
            "log_type": "bot",
            "job_id": str(self.job.id),
            "task_id": "task123",
            "project_id": str(self.project.id),
            "files": [SimpleUploadedFile("file1.txt", b"file_content")]
        }
        self.fuzzer_log_data = {
            "log_type": "fuzzer",
            "job_id": str(self.job.id),
            "fuzzer_id": str(self.fuzzer.id),
            "project_id": str(self.project.id),
            "date": "2023-10-10",
            "files": [SimpleUploadedFile("file1.txt", b"file_content")]
        }

    @patch('PinguApi.subtasks.storage.logs.store_logs.delay')
    def test_upload_bot_logs(self, mock_store_logs):
        # Make the POST request
        response = self.client.post(
            path=self.upload_url,
            data=self.bot_log_data,
            format='multipart'  # Use format='multipart' instead of content_type
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_store_logs.assert_called_once()

    @patch('PinguApi.subtasks.storage.logs.store_logs.delay')
    def test_upload_fuzzer_logs(self, mock_store_logs):
        response = self.client.post(self.upload_url, self.fuzzer_log_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_store_logs.assert_called_once()

class DownloadLogsViewTests(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[0].key)
        
        self.project = init_test_project()
        self.fuzzer, fuzzer_zip = init_test_Fuzzer(self.project)
        self.job = init_test_Job(self.project)
        
        self.download_url = '/api/storage/logs/download/'

    @patch('PinguApi.subtasks.storage.logs.download_logs.apply')
    def test_download_bot_logs(self, mock_download_logs):
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("testfile1.txt", "dummy content 1")
            zip_file.writestr("testfile2.txt", "dummy content 2")
        zip_stream.seek(0)
        
        mock_result = MagicMock()
        mock_result.get.return_value = zip_stream
        mock_download_logs.return_value = mock_result
        
        response = self.client.get(self.download_url, {
            "log_type": "bot",
            "job_id": str(self.job.id),
            "task_id": "task123",
            "project_id": str(self.project.id)
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check ZIP contents
        # Check ZIP contents
        zip_bytes = b''.join(response.streaming_content)
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zip_ref:
            file_list = zip_ref.namelist()
            self.assertEqual(sorted(file_list), ["testfile1.txt", "testfile2.txt"])

    @patch('PinguApi.subtasks.storage.logs.download_logs.apply')
    def test_download_fuzzer_logs(self, mock_download_logs):
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("testfile1.txt", "dummy content 1")
            zip_file.writestr("testfile2.txt", "dummy content 2")
        zip_stream.seek(0)
        
        mock_result = MagicMock()
        mock_result.get.return_value = zip_stream
        mock_download_logs.return_value = mock_result
        
        response = self.client.get(self.download_url, {
            "log_type": "fuzzer",
            "job_id": str(self.job.id),
            "fuzzer_id": str(self.fuzzer.id),
            "project_id": str(self.project.id),
            "date": "2023-10-10"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check ZIP contents
        # Check ZIP contents
        zip_bytes = b''.join(response.streaming_content)
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zip_ref:
            file_list = zip_ref.namelist()
            self.assertEqual(sorted(file_list), ["testfile1.txt", "testfile2.txt"])
