import base64
import io
import logging
import zipfile
from celery import shared_task
from celery.utils.log import get_task_logger
import os
from PinguApi.handlers.storage_handlers.fuzzer import FuzzerStorage

logger = logging.getLogger(__name__)

# Fuzzers Tasks
@shared_task(name="upload_fuzzer_to_bucket")
def upload_fuzzer_to_bucket(file, bucket_name):
    try:
        fuzzer_storage = FuzzerStorage(bucket_name=bucket_name)
        file_content = base64.b64decode(file["content"])
              
        fuzzer_storage.upload_fuzzer_from_cache(file_content, file["name"]) 
        logger.info("upload_fuzzer_to_bucket")
        
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_fuzzer_from_bucket")
def download_fuzzer_from_bucket(storage_path):
    try:
        bucket_name, file_path = storage_path.split("/")
        fuzzer_storage = FuzzerStorage(bucket_name=bucket_name)
    
        if not os.path.exists(fuzzer_storage.cache_path):
            os.makedirs(os.path.dirname(fuzzer_storage.cache_path), exist_ok=True)
    
        fuzzer_storage.download_fuzzer_to_cache(file_path)
    
        # Step 3: Create an in-memory file
        with (open(f"{fuzzer_storage.cache_path}/{os.path.basename(file_path)}", 'rb')) as f:
            return io.BytesIO(f.read())
        
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_fuzzer_from_bucket")
def remove_fuzzer_from_bucket(storage_path):
    try:
        bucket_name, file_path = storage_path.split("/")
        fuzzer_storage = FuzzerStorage(bucket_name=bucket_name)
        fuzzer_storage.delete_fuzzer(file_path)
        logger.info("remove_fuzzer_from_bucket")
    except Exception as e:
        logger.error(e)

@shared_task(name="get_fuzzer_from_cache")
def get_fuzzer_from_cache(storage_path) -> io.BytesIO:
    try:
        bucket_name, file_path = storage_path.split("/")
        fuzzer_storage = FuzzerStorage(bucket_name=bucket_name)
        
        if not os.path.exists(fuzzer_storage.cache_path):
            os.makedirs(os.path.dirname(fuzzer_storage.cache_path), exist_ok=True)
    
        fuzzer_storage.download_fuzzer_to_cache(file_path)
        
        # Construct the full path to the file in the cache
        cached_file_path = os.path.join(fuzzer_storage.cache_path, file_path)
        logger.info(f"Cached file path: {cached_file_path}")
        
        f = open(cached_file_path, 'rb')
        file_content = f.read()
        f.close()
        logger.info(f"Read {len(file_content)} bytes from cached file")
        zip_buffer = io.BytesIO(file_content)
        try:
            with zipfile.ZipFile(zip_buffer, 'r') as zipf:
                zipf.testzip()  # This will raise an exception if the ZIP file is not valid
        except zipfile.BadZipFile:
            raise Exception("Invalid ZIP file")

        return zip_buffer

        
    except Exception as e:
        logger.error(e)