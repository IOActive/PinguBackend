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
        
    
@shared_task(name="download_fuzzer_from_bucket")
def download_fuzzer_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.get_object(bucketName=bucket_name, fileName=fileName)
        logger.info("download_fuzzer_from_bucket")
        return result.data
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_fuzzer_from_bucket")
def remove_fuzzer_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.remove_object(bucketName=bucket_name, fileName=fileName)
        logger.info("remove_fuzzer_from_bucket")
        return result
    except Exception as e:
        logger.error(e)