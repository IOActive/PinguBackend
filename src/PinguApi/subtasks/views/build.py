import base64
import io
import logging
import zipfile
from celery import shared_task
from celery.utils.log import get_task_logger
import os
from PinguApi.handlers.storage_handlers.build import BuildStorage

logger = logging.getLogger(__name__)

# Builds Tasks
@shared_task(name="upload_build_to_bucket")
def upload_build_to_bucket(file, bucket_name):
    try:
        build_storage = BuildStorage(bucket_name=bucket_name)
        file_content = base64.b64decode(file["content"])
              
        build_storage.upload_build_from_cache(file_content, file["name"])
        target_list_stream = build_storage.get_target_list()
        
        if not target_list_stream:
            build_storage.create_target_list()
            build_storage.write_targets_list(f'{file["name"]}\n'.encode('utf-8'))
            
        else:
            target_list_stream += f'{file["name"]}\n'.encode('utf-8')
            build_storage.write_targets_list(target_list_stream)
            
        logger.info("upload_build_to_bucket")
        
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_build_from_bucket")
def download_build_from_bucket(storage_path):
    try:
        bucket_name, file_path = storage_path.split("/")
        build_storage = BuildStorage(bucket_name=bucket_name)
    
        if not os.path.exists(build_storage.cache_path):
            os.makedirs(os.path.dirname(build_storage.cache_path), exist_ok=True)
    
        build_storage.download_build_to_cache(file_path)
    
        # Step 3: Create an in-memory file
        with (open(f"{build_storage.cache_path}/{os.path.basename(file_path)}", 'rb')) as f:
            return io.BytesIO(f.read())
        
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_build_from_bucket")
def remove_build_from_bucket(storage_path):
    try:
        bucket_name, file_name = storage_path.split("/")
        build_storage = BuildStorage(bucket_name=bucket_name)
        build_storage.delete_build(build_file=file_name)
        
        target_list_stream = build_storage.get_target_list()
        if target_list_stream:
            target_list = target_list_stream.decode('utf-8').split('\n')
            target_list = [entry for entry in target_list if entry != os.path.basename(file_name)]
            build_storage.write_targets_list('\n'.join(target_list).encode('utf-8'))
        
        logger.info("remove_build_from_bucket")
    except Exception as e:
        logger.error(e)

@shared_task(name="get_build_from_cache")
def get_build_from_cache(bucket_name, file_path):
    try:
        build_storage = BuildStorage(bucket_name=bucket_name)
        
        if not os.path.exists(build_storage.cache_path):
            os.makedirs(os.path.dirname(build_storage.cache_path), exist_ok=True)
    
        build_storage.download_build_to_cache(file_path)

        f = open(f"{build_storage.cache_path}/{file_path}", 'rb')
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