# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from PinguApi.utils.MinioManager import MinioManger
import zipfile
import io

logger = get_task_logger(__name__)


@shared_task(name="upload_fuzzer_to_bucket")
def upload_fuzzer_to_bucket(zip_file_stream, zip_filename):
    try:
        file_stream = io.BytesIO(zip_file_stream)
        size_in_bytes = len(file_stream.getbuffer())
        
        bucket_client = MinioManger()
        result = bucket_client.put_object(bucketName="fuzzers", name=zip_filename, data=file_stream, size=size_in_bytes)
        logger.info("upload_fuzzer_to_bucket")
        blobstore_path = f"{result.bucket_name}/{result.object_name}"
        
        return blobstore_path, size_in_bytes
    except Exception as e:
        logger.error(e)
        
    
    