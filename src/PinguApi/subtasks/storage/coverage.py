import base64
from typing import Dict, List
from celery import shared_task
from celery.utils.log import get_task_logger
import os
from PinguApi.handlers.storage_handlers.coverage import CoverageStorage

logger = get_task_logger(__name__)

@shared_task(name="store_coverage")
def store_coverage(bucket_name, storage_path, files:List[Dict]):
    coverage_storage = CoverageStorage(bucket_name=bucket_name, bucket_path=storage_path)
    
    if not os.path.exists(coverage_storage.cache_path):
        os.makedirs(coverage_storage.cache_path, exist_ok=True)
    
    for file in files:
        cache_file_path = os.path.join(coverage_storage.cache_path, file['name'])
        file_content = base64.b64decode(file["content"])
        with open(cache_file_path, 'wb') as f:
            f.write(file_content)
            
    coverage_storage.rsync_from_disk(storage_path)
    
