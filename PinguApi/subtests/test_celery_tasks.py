from django.test import TestCase
from PinguApi.tasks import upload_fuzzer_to_bucket

class AsyncTaskTests(TestCase):
    def setUp(self):
        self.fuzzer_zip = open('PinguApi/subtests/test.zip', 'rb').read()

        
    def test_upload_fuzzer_to_bucket(self):
        # Call the Celery shared task synchronously using apply()
        blobstore_path, size_in_bytes = upload_fuzzer_to_bucket.apply(args=[self.fuzzer_zip, "test_fuzzer.zip"]).get()
        # Assertions to check the task result
        self.assertNotEquals(blobstore_path, "")
        self.assertNotEquals(size_in_bytes, 0)

