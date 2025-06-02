import base64
from typing import Dict, List
from celery import shared_task
from celery.utils.log import get_task_logger
import os
import io
import zipfile
from PinguApi.handlers.storage_handlers.corpus import CorpusStorage

logger = get_task_logger(__name__)

@shared_task(name="store_corpus")
def store_corpus(bucket_name, storage_path, files:List[Dict]):
    corpus_storage = CorpusStorage(bucket_name=bucket_name, bucket_path=storage_path)
    
    if not os.path.exists(corpus_storage.cache_path):
        os.makedirs(corpus_storage.cache_path, exist_ok=True)
    
    for file in files:
        cache_file_path = os.path.join(corpus_storage.cache_path, file['name'])
        file_content = base64.b64decode(file["content"])
        with open(cache_file_path, 'wb') as f:
            f.write(file_content)
            
    corpus_storage.rsync_from_disk(storage_path)
    
    

    
@shared_task(name="download_corpus")
def download_corpus(bucket_name, storage_path) -> io.BytesIO:
    """
    Syncs a storage folder to the local cache (if valid), streams it as a ZIP file, and returns it to the view handler.
    """
    try:
        # Step 2: Ensure the folder is synced (sync_folder_from handles cache)
        corpus_storage = CorpusStorage(bucket_name=bucket_name, bucket_path=storage_path)
        
        success = corpus_storage.rsync_to_disk(storage_path)
        
        if not success:
            logger.error(f"Failed to sync folder: {storage_path}")
            return None

        # Step 3: Create an in-memory ZIP stream
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(corpus_storage.cache_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, corpus_storage.cache_path)  # Maintain folder structure
                    zip_file.write(file_path, arcname)

        # Step 4: Reset stream position for reading
        zip_stream.seek(0)
        
        return zip_stream

    except Exception as e:
        logger.error(f"Error while streaming zipped folder {storage_path}: {e}")
        return None
