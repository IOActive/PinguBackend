# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PinguApi.utils.MinioManager import MinioManger
from PinguApi.tasks import upload_corpus_to_bucket, upload_fuzzer_to_bucket, download_fuzzer_from_bucket, remove_fuzzer_from_bucket, download_bot_logs, \
    upload_custom_binary_to_bucket, remove_custom_binary_from_bucket, upload_build_to_bucket, download_build_from_bucket, remove_build_from_bucket
from minio.helpers import ObjectWriteResult
from unittest.mock import MagicMock, ANY, patch
from django.test import TestCase


class TaskTests(TestCase):
    
    def setUp(self) -> None:
        self.test_zip = open('PinguApi/subtests/test.zip', 'rb').read()
    
    @patch.object(MinioManger, 'put_object')
    def test_upload_fuzzer_to_bucket(self, mock_put_object: MagicMock):
        # Create a BytesIO object with some test data
        file_stream = self.test_zip

        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.bucket_name = 'test_bucket'
        mock_result.object_name = 'test_object'
        mock_result.version_id = 'test_version'
        mock_result.etag = 'test_etag'
        mock_result.last_modified = 'test_last_modified'

        # Set the return value of the mock_put_object method
        mock_put_object.return_value = mock_result


        # Call the upload_fuzzer_to_bucket function
        result = upload_fuzzer_to_bucket(file_stream, 'test.zip')

        # Assert that the put_object method was called with the correct arguments
        mock_put_object.assert_called_once()

        # Assert that the function returned the correct values
        assert result == ('test_bucket/test_object', 212)
        
        remove_fuzzer_from_bucket("fuzzers/test.zip")
    
    @patch.object(MinioManger, 'get_object')
    def test_download_fuzzer_from_bucket(self, mock_get_object):
        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.data = open('PinguApi/subtests/test.zip', 'rb').read()

        # Set the return value of the mock_put_object method
        mock_get_object.return_value = mock_result
        
        result = download_fuzzer_from_bucket("fuzzers/test.zip")
        
        assert result == self.test_zip
        
    @patch.object(MinioManger, 'remove_object')
    def test_remove_fuzzer_from_bucket(self, mock_remove_object):
        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result = None
        # Set the return value of the mock_put_object method
        mock_remove_object.return_value = mock_result
        result = remove_fuzzer_from_bucket("fuzzers/test.zip")
        assert result == None

    @patch.object(MinioManger, 'get_object')
    def test_download_bot_logs(self, mock_get_object):
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.data = "Empty"
        # Set the return value of the mock_put_object method
        mock_get_object.return_value = mock_result
        logs = download_bot_logs(bot_id='4e63f439-1e3d-4ccb-a193-c47188a85ab9')
        assert len(logs) > 0
        
    @patch.object(MinioManger, 'put_object')
    def test_upload_custom_binary_to_bucket(self, mock_put_object: MagicMock):
        # Create a BytesIO object with some test data
        file_stream = self.test_zip

        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.bucket_name = 'test_bucket'
        mock_result.object_name = 'test_object'
        mock_result.version_id = 'test_version'
        mock_result.etag = 'test_etag'
        mock_result.last_modified = 'test_last_modified'

        # Set the return value of the mock_put_object method
        mock_put_object.return_value = mock_result

        # Call the upload_fuzzer_to_bucket function
        result = upload_custom_binary_to_bucket(file_stream, 'test.zip')

        # Assert that the put_object method was called with the correct arguments
        mock_put_object.assert_called_once()

        # Assert that the function returned the correct values
        assert result == ('test_bucket/test_object', 212)
        
        remove_fuzzer_from_bucket("fuzzers/test.zip")
    
    @patch.object(MinioManger, 'remove_object')
    def test_remove_custom_binary_from_bucket(self, mock_remove_object):
        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result = None
        # Set the return value of the mock_put_object method
        mock_remove_object.return_value = mock_result
        result = remove_custom_binary_from_bucket("fuzzers/test.zip")
        assert result == None
        
    @patch.object(MinioManger, 'put_object')
    def test_upload_corpus_to_bucket(self, mock_put_object: MagicMock):
        # Create a BytesIO object with some test data
        file_stream = self.test_zip

        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.bucket_name = 'test_bucket'
        mock_result.object_name = 'test_object'
        mock_result.version_id = 'test_version'
        mock_result.etag = 'test_etag'
        mock_result.last_modified = 'test_last_modified'

        # Set the return value of the mock_put_object method
        mock_put_object.return_value = mock_result

        # Call the upload_fuzzer_to_bucket function
        result = upload_corpus_to_bucket(file_stream, "test_project", "test_fuzzer", "test_fuzzTarget")

        # Assert that the put_object method was called with the correct arguments
        mock_put_object.assert_called_once()

        # Assert that the function returned the correct values
        assert result == ('test_bucket/test_object', 28)
        
    @patch.object(MinioManger, 'put_object')
    def test_upload_build_to_bucket(self, mock_put_object: MagicMock):
        # Create a BytesIO object with some test data
        file_stream = self.test_zip

        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.bucket_name = 'test_bucket'
        mock_result.object_name = 'test_object'
        mock_result.version_id = 'test_version'
        mock_result.etag = 'test_etag'
        mock_result.last_modified = 'test_last_modified'

        # Set the return value of the mock_put_object method
        mock_put_object.return_value = mock_result

        # Call the upload_fuzzer_to_bucket function
        result = upload_build_to_bucket(file_stream, "test_build", "Release")

        # Assert that the put_object method was called with the correct arguments
        mock_put_object.assert_called_once()

        # Assert that the function returned the correct values
        assert result == ('test_bucket/test_object', 212)

    @patch.object(MinioManger, 'get_object')
    def test_download_build_from_bucket(self, mock_get_object):
        
        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result.data = open('PinguApi/subtests/test.zip', 'rb').read()

        # Set the return value of the mock_put_object method
        mock_get_object.return_value = mock_result
                
        result = download_build_from_bucket("fuzzers/test.zip")
        
        assert result == self.test_zip
                
    @patch.object(MinioManger, 'remove_object')
    def test_remove_build_from_bucket(self, mock_remove_object):
        # Create a mocked ObjectWriteResult object
        mock_result = MagicMock(spec=ObjectWriteResult)
        mock_result = None
        # Set the return value of the mock_put_object method
        mock_remove_object.return_value = mock_result
        result = remove_build_from_bucket("fuzzers/test.zip")
        assert result == None
