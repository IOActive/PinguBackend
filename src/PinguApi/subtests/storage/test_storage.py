import datetime
import unittest
from unittest.mock import MagicMock, patch
from PinguApi.storage_providers.storage_provider import StorageProvider
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.models import Project
from PinguApi.handlers import storage

class TestStorageFunctions(PinguAPITestCase):
    
    def setUp(self):
        # Mock the settings
        self.settings_patcher = patch('django.conf.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.LOCAL_STORAGE_PATH = '/tmp/storage'
        self.mock_settings.MINIO_HOST = 'localhost'
        self.mock_settings.MINIO_ACCESS_KEY = 'test_key'
        self.mock_settings.MINIO_SECRET_KEY = 'test_secret'
        
        # Mock the provider
        self.mock_provider = MagicMock(spec=StorageProvider)
        self.provider_patcher = patch('PinguApi.handlers.storage._provider', return_value=self.mock_provider)
        self.provider_patcher.start()

    def tearDown(self):
        self.settings_patcher.stop()
        self.provider_patcher.stop()


    def test_create_bucket_if_needed_exists(self):
        self.mock_provider.get_bucket.return_value = True
        result = storage.create_bucket_if_needed('test-bucket')
        self.assertTrue(result)
        self.mock_provider.create_bucket.assert_not_called()

    def test_create_bucket_if_needed_new(self):
        self.mock_provider.get_bucket.return_value = False
        self.mock_provider.create_bucket.return_value = True
        with patch('time.sleep') as mock_sleep:
            result = storage.create_bucket_if_needed('test-bucket')
            self.assertTrue(result)
            self.mock_provider.create_bucket.assert_called_once()
            mock_sleep.assert_called_once_with(storage.CREATE_BUCKET_DELAY)

    def test_copy_file_from_success(self):
        self.mock_provider.copy_file_from.return_value = True
        result = storage.copy_file_from('storage/path')
        self.assertTrue(result)
        self.mock_provider.copy_file_from.assert_called_once_with(
            'storage/path',
            './tmp/cache/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855/path'
        )

    def test_copy_file_to_file_not_exists(self):
        with patch('os.path.exists', return_value=False):
            with patch('logging.error') as mock_logger:
                result = storage.copy_file_to('nonexistent/path', 'storage/path')
                self.assertFalse(result)

    def test_copy_file_to_success(self):
        with patch('os.path.exists', return_value=True):
            self.mock_provider.copy_file_to.return_value = True
            result = storage.copy_file_to('local/path', 'storage/path')
            self.assertTrue(result)
            self.mock_provider.copy_file_to.assert_called_once()

    def test_copy_blob(self):
        self.mock_provider.copy_blob.return_value = True
        result = storage.copy_blob('source/path', 'target/path')
        self.assertTrue(result)
        self.mock_provider.copy_blob.assert_called_once_with('source/path', 'target/path')

    def test_delete(self):
        self.mock_provider.delete.return_value = True
        result = storage.delete('storage/path')
        self.assertTrue(result)
        self.mock_provider.delete.assert_called_once_with('storage/path')

    def test_exists_success(self):
        self.mock_provider.get.return_value = {'size': 100}
        result = storage.exists('storage/path')
        self.assertTrue(result)

    def test_exists_failure(self):
        self.mock_provider.get.return_value = False
        result = storage.exists('storage/path')
        self.assertFalse(result)

    def test_last_updated(self):
        mock_blobs = [
            {'updated': datetime.datetime.fromisoformat('2023-01-01T00:00:00Z')},
            {'updated': datetime.datetime.fromisoformat('2023-01-02T00:00:00Z')}
        ]
        self.mock_provider.list_blobs.return_value = mock_blobs
        result = storage.last_updated('storage/path')
        self.assertIsNotNone(result)

    def test_blobs_bucket(self):
        mock_project = MagicMock(spec=Project)
        mock_project.configuration = 'blobs:\n  bucket: test-bucket'
        with patch('yaml.safe_load') as mock_yaml:
            mock_yaml.return_value = {'blobs': {'bucket': 'test-bucket'}}
            result = storage.blobs_bucket(mock_project)
            self.assertEqual(result, 'test-bucket')
