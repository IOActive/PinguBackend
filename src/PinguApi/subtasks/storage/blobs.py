import base64

from celery import shared_task
from celery.utils.log import get_task_logger
import os
import io
from PinguApi.handlers.storage_handlers.blobs import BlobsStorage

logger = get_task_logger(__name__)

@shared_task(name="downlaod_blob")
def download_blob(bucket_name, key):
    """Download a blob from the bucket."""
    blobs_storage = BlobsStorage(bucket_name)
    
    if not os.path.exists(blobs_storage.cache_path):
        os.makedirs(os.path.dirname(blobs_storage.cache_path), exist_ok=True)
    
    blobs_storage.read_blob_to_disk(key)
    
    with open(f"{blobs_storage.cache_path}/{key}", "rb") as f:
        return io.BytesIO(f.read())
    
@shared_task(name="read_blob")
def read_blob(bucket_name, key):
    """Read a blob from the bucket."""
    blobs_storage = BlobsStorage(bucket_name)
    if not os.path.exists(blobs_storage.cache_path):
        os.makedirs(os.path.dirname(blobs_storage.cache_path), exist_ok=True)
    
    blobs_storage.read_blob_to_disk(key)
    
    with open(f"{blobs_storage.cache_path}/{key}", "rb") as f:
        return io.BytesIO(f.read())
    
@shared_task(name="write_blob")
def write_blob(bucket_name, key, blob, metadata):
    """Write a blob to the bucket."""
    blobs_storage = BlobsStorage(bucket_name)
    if not os.path.exists(blobs_storage.cache_path):
        os.makedirs(blobs_storage.cache_path, exist_ok=True)
    
    blob_content = base64.b64decode(blob["content"])

    blobs_storage.write_blob(blob_content, key, metadata=metadata)
    
@shared_task(name="delete_blob")
def delete_blob(bucket_name, key):
    try:
        blobs_storage = BlobsStorage(bucket_name=bucket_name)
        blobs_storage.remove_blob(key)
        logger.info("remove_custom_binary_from_bucket: Custom binary removed successfully")
    except Exception as e:
        logger.error(e)
