import os
from pathlib import Path
import unittest
from PinguApi.storage_providers.minio_provider import MinioProvider
from minio.datatypes import Bucket, Object
from unittest import mock
import datetime
from pyfakefs.fake_filesystem_unittest import TestCase

class TestMinioProvider(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.provider  = MinioProvider('minio.io', 'accessKey', 'secretKey')

    @mock.patch('minio.Minio.make_bucket')
    def test_create_bucket(self, mock_make_bucket):
        mock_make_bucket.return_value = True
        r = self.provider.create_bucket('test2')
        assert r is True

    @mock.patch('minio.Minio.list_buckets')
    def test_get_bucket(self, mock_list_buckets):
        mock_list_buckets.return_value = [Bucket('test', datetime.datetime.now())]

        bucket = self.provider.get_bucket('test')
        assert bucket is not None

    @mock.patch('minio.Minio.list_objects')
    def test_list_blobs(self, mock_list_objects):
        objects = [
            {'bucket_name': 'my_bucket', 'object_name': 'folder/file1.txt', 'last_modified': '2022-01-01T00:00:00Z', 'size': 1024},
            {'bucket_name': 'my_bucket', 'object_name': 'folder/subfolder/file2.txt', 'last_modified': '2022-01-01T00:00:00Z', 'size': 2048}
        ]
        mock_list_objects.return_value = [Object(**obj) for obj in objects]

        remote_path = 'http://minio.io/my_bucket/folder/'  # Assuming this is the correct remote path format for your storage provider
        expected_results = [
            {'bucket': 'my_bucket', 'name': 'folder/file1.txt', 'updated': '2022-01-01T00:00:00Z', 'size': 1024},
            {'bucket': 'my_bucket', 'name': 'folder/subfolder/file2.txt', 'updated': '2022-01-01T00:00:00Z', 'size': 2048},
        ]

        for i, result in enumerate(self.provider.list_blobs(remote_path, recursive=True)):
            self.assertDictEqual(result, expected_results[i])  # Compare individual results with expected

    @mock.patch('minio.Minio.list_objects')
    def test_list_blobs_non_recursive(self, mock_list_objects):
        objects = [
            {'bucket_name': 'my_bucket', 'object_name': 'folder/file1.txt', 'last_modified': '2022-01-01T00:00:00Z', 'size': 1024},
            {'bucket_name': 'my_bucket', 'object_name': 'folder/subfolder/file2.txt', 'last_modified': '2022-01-01T00:00:00Z', 'size': 2048}
        ]
        mock_list_objects.return_value = [Object(**obj) for obj in objects]

        remote_path = 'http://minio.io/my_bucket/folder/'  # Assuming this is the correct remote path format for your storage provider
        expected_results = [
            {'bucket': 'my_bucket', 'name': 'folder/file1.txt'},
            {'bucket': 'my_bucket', 'name': 'folder/subfolder/file2.txt'},
        ]

        for i, result in enumerate(self.provider.list_blobs(remote_path, recursive=False)):
            self.assertDictEqual(result, expected_results[i])  # Compare individual results with expected

    @mock.patch('minio.Minio.fget_object')
    def test_copy_file_from(self, mock_fget_object):
        mock_fget_object.return_value = Object(bucket_name='test', object_name='test_o')  # Mock the return value of fget_object to None for this test
        r = self.provider.copy_file_from("test/test2/values.yaml", "../../../../bot/tmp/")
        assert r is True

    @mock.patch('minio.Minio.fput_object')
    @mock.patch('minio.Minio.put_object')
    def test_copy_file_to(self, mock_put_object, mock_fput_object):
        mock_fput_object.return_value = Object(bucket_name='test', object_name='test_o')  # Mock the return value of fget_object to None for This test
        mock_put_object.return_value = Object(bucket_name='test', object_name='test_o')  # Mock the return value of fget_object to None for this test
        r = self.provider.copy_file_to("../../../../bot/tmp/test2/values.yaml", "/test/test2/values2.yaml")
        assert r is True

    @mock.patch('minio.Minio.copy_object')
    def test_copy_blob(self, mock_copy_object):
        mock_copy_object.return_value = Object(bucket_name='test', object_name='test_o')  # Mock the return value of fget_object to None for this test
        r = self.provider.copy_blob("test/test2/values.yaml", "/test/values2.yaml")
        assert r is True

    @mock.patch('minio.Minio.get_object')
    def test_read_data(self, mock_get_object):
        mock_get_object.return_value = mock.MagicMock(data=b'aaaa')
        data = self.provider.read_data("test/test2/values.yaml")
        assert len(data) > 0

    @mock.patch('minio.Minio.put_object')
    def test_write_data(self, mock_put_object):
        mock_put_object.return_value = mock.MagicMock(object_name='test', etag='tag', version_id=1)
        r = self.provider.write_data(remote_path="/test/target.list", data="openssl-1.0.1f.zip")
        assert r is True

    @mock.patch('minio.Minio.stat_object')
    def test_get(self, mock_stat_object):
        mock_stat_object.return_value = mock.MagicMock(last_modified=datetime.datetime.now(), size=1)
        r = self.provider.get(remote_path="test/test2/values.yaml")
        assert r is not None

    @mock.patch('minio.Minio.remove_object')
    def test_delete(self, mock_remove_object):
        mock_remove_object.return_value = True
        r = self.provider.delete(remote_path="test/test2/values.yaml")
        assert r is True

    @mock.patch('os.remove')
    @mock.patch('minio.Minio.list_objects')
    @mock.patch('minio.Minio.fget_object')
    def test_sync_folder_from(self, mock_fget_object, mock_list_objects, os_remove):
        objects = [
            {'bucket_name': 'my_bucket', 'object_name': 'folder/file1.txt'},
            {'bucket_name': 'my_bucket', 'object_name': 'folder/file2.txt'}
        ]
        mock_list_objects.return_value = [Object(**obj) for obj in objects]
        mock_fget_object.return_value = Object(bucket_name='my_bucket', object_name='folder/file1.txt')

        self.fs.create_file('/local/path/folder/file2.txt')
        self.fs.create_file('/local/path/folder/file3.txt')

        self.provider.sync_folder_from('/local/path', 'http://minio.io/my_bucket/folder/', delete=True)
        mock_list_objects.assert_called_with('my_bucket', prefix='folder/', recursive=True)
        mock_fget_object.assert_called()
        os_remove.assert_called_with('/local/path/folder/file3.txt')
        self.assertTrue(os_remove.called)
        

    @mock.patch('minio.Minio.remove_object')
    @mock.patch('minio.Minio.list_objects')
    @mock.patch('minio.Minio.fput_object')
    @mock.patch('minio.Minio.put_object')
    def test_sync_folder_to(self, mock_put_object, mock_fput_object, mock_list_objects, mock_remove_object):
        objects = [
            {'bucket_name': 'my_bucket', 'object_name': 'folder/file1.txt'},
            {'bucket_name': 'my_bucket', 'object_name': 'folder/file2.txt'}
        ]
        mock_list_objects.return_value = [Object(**obj) for obj in objects]
        mock_fput_object.return_value = Object(bucket_name='my_bucket', object_name='folder/file1.txt')
        mock_put_object.return_value = Object(bucket_name='my_bucket', object_name='folder/file1.txt')
        mock_remove_object.return_value = True

        self.fs.create_file('/local/path/file1.txt')

        with mock.patch('os.path.isfile', return_value=True):
            with mock.patch('pathlib.Path.rglob', return_value=[Path('/local/path/file1.txt')]):
                self.provider.sync_folder_to('http://minio.io/my_bucket/folder/', '/local/path', delete=True)
                mock_list_objects.assert_called_with('my_bucket', prefix='folder/', recursive=True)
                mock_fput_object.assert_called()
                mock_remove_object.assert_called_with('my_bucket', 'folder/file2.txt')
                self.assertTrue(mock_remove_object.called)