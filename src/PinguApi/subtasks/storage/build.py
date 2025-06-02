import zipfile
from celery import shared_task
from celery.utils.log import get_task_logger
import os
import io
from PinguApi.handlers.storage_handlers.build import BuildStorage


@shared_task(name="download_build")
def download_build(bucket_name, file_path) -> io.BytesIO:
    build_storage = BuildStorage(bucket_name=bucket_name)
    
    if not os.path.exists(build_storage.cache_path):
        os.makedirs(build_storage.cache_path, exist_ok=True)
    
    build_storage.download_build_to_cache(file_path)
    
    # Construct the full path to the file in the cache
    cached_file_path = f"{build_storage.cache_path}/{file_path}"
    
    with open(cached_file_path, 'rb') as f:
        file_content = f.read()
        zip_buffer = io.BytesIO(file_content)
        try:
            with zipfile.ZipFile(zip_buffer, 'r') as zipf:
                zipf.testzip()  # This will raise an exception if the ZIP file is not valid
        except zipfile.BadZipFile:
            raise Exception("Invalid ZIP file")

        return zip_buffer

@shared_task(name="get build list")
def get_build_list(bucket_name):
    build_storage = BuildStorage(bucket_name=bucket_name)
    
    return build_storage.get_target_list()

@shared_task(name="get build size")
def get_build_size(bucket_name, storage_path):
    build_storage = BuildStorage(bucket_name=bucket_name, bucket_path=storage_path)
    
    return build_storage.get_build_size(storage_path)