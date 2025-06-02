import base64
from typing import Dict, List
import zipfile
from celery import shared_task
from celery.utils.log import get_task_logger
import os
import io
from PinguApi.handlers.storage_handlers.logs import LogsStorage

logger = get_task_logger(__name__)

@shared_task(name="store_logs")
def store_logs(bucket_name, storage_path, files: List[Dict]):
    logs_storage = LogsStorage(bucket_name=bucket_name, bucket_path=storage_path)
    logger.info(f"Cache Local directory {logs_storage.cache_path}")
    if not os.path.exists(logs_storage.cache_path):
        os.makedirs(logs_storage.cache_path, exist_ok=True)
    
    for file in files:
        cache_file_path = os.path.join(logs_storage.cache_path, file['name'])
        file_content = base64.b64decode(file["content"])
        with open(cache_file_path, 'wb') as f:
            f.write(file_content)
            
    logs_storage.rsync_from_disk(file_content)
    return True

@shared_task(name="download_logs")
def download_logs(bucket_name, storage_path) -> io.BytesIO:
    """
    Syncs a storage folder to the local cache (if valid), streams it as a ZIP file, and returns it to the view handler.
    """
    try:
        logs_storage = LogsStorage(bucket_name=bucket_name, bucket_path=storage_path)
        
        if not os.path.exists(logs_storage.cache_path):
            os.makedirs(os.path.dirname(logs_storage.cache_path), exist_ok=True)
        
        success = logs_storage.rsync_to_disk()
        
        if not success:
            logger.error(f"Failed to sync folder: {storage_path}")
            return None

        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(logs_storage.cache_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, logs_storage.cache_path)
                    zip_file.write(file_path, arcname)

        zip_stream.seek(0)
        
        return zip_stream

    except Exception as e:
        logger.error(f"Error while streaming zipped folder {storage_path}: {e}")
        return None
