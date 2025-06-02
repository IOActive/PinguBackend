import base64
from typing import Dict, List
from celery import shared_task
from celery.utils.log import get_task_logger
import os
from PinguApi.handlers.storage_handlers.stats import StatsStorage

logger = get_task_logger(__name__)


@shared_task(name="store_stats")
def store_stats(bucket_name, storage_path, files:List[Dict]):
    stats_storage = StatsStorage(bucket_name=bucket_name, bucket_path=storage_path)
    
    if not os.path.exists(stats_storage.cache_path):
        os.makedirs(stats_storage.cache_path, exist_ok=True)
    
    for file in files:
        cache_file_path = os.path.join(stats_storage.cache_path, file['name'])
        file_content = base64.b64decode(file["content"])
        with open(cache_file_path, 'wb') as f:
            f.write(file_content)
            
    stats_storage.rsync_from_disk(storage_path)
    return True
    