from PinguApi.utils.MinioManager import MinioManger
from PinguApi.tasks import upload_fuzzer_to_bucket, download_fuzzer_from_bucket, remove_fuzzer_from_bucket
from minio.helpers import ObjectWriteResult
from unittest.mock import MagicMock, ANY, patch
from django.test import TestCase


class TaskTests(TestCase):
    
    def setUp(self) -> None:
        self.fuzzer_zip = open('PinguApi/subtests/test.zip', 'rb').read()
    
    @patch.object(MinioManger, 'put_object')
    def test_upload_fuzzer_to_bucket(self, mock_put_object: MagicMock):
        # Create a BytesIO object with some test data
        file_stream = self.fuzzer_zip

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
    
    def test_download_fuzzer_from_bucket(self):
        
        upload_fuzzer_to_bucket(self.fuzzer_zip, 'test.zip')
        
        result = download_fuzzer_from_bucket("fuzzers/test.zip")
        
        assert result == self.fuzzer_zip
        
        remove_fuzzer_from_bucket("fuzzers/test.zip")
        
    def test_remove_fuzzer_from_bucket(self):
        upload_fuzzer_to_bucket(self.fuzzer_zip, 'test.zip')
        result = remove_fuzzer_from_bucket("fuzzers/test.zip")
        assert result == None