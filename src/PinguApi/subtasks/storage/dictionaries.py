import base64

from celery import shared_task
from celery.utils.log import get_task_logger
import os
import io
from PinguApi.handlers.storage_handlers.dictionaries import DictionariesStorage

logger = get_task_logger(__name__)

@shared_task(name="downlaod_dictionary")
def download_dictionary(bucket_name, storage_path, dic_file):
    """Download a dictionary from the bucket."""
    dictionarys_storage = DictionariesStorage(bucket_name=bucket_name, bucket_path=storage_path)
    
    if not os.path.exists(dictionarys_storage.cache_path):
        os.makedirs(os.path.dirname(dictionarys_storage.cache_path), exist_ok=True)
    
    dictionarys_storage.read_dictionary_to_disk(dic_file)
    
    f = open(f"{dictionarys_storage.cache_path}/{dic_file}", 'rb')
    file_content = f.read()
    f.close()
    logger.info(f"Read {len(file_content)} bytes from cached file")
    return io.BytesIO(file_content)
    
@shared_task(name="write_dictionary")
def upload_dictionary(bucket_name, storage_path, blob, metadata=""):
    """Write a dictionary to the bucket."""
    dictionarys_storage = DictionariesStorage(bucket_name, storage_path)
    if not os.path.exists(dictionarys_storage.cache_path):
        os.makedirs(dictionarys_storage.cache_path, exist_ok=True)
    
    dictionary_content = base64.b64decode(blob["content"])

    dictionarys_storage.write_dictionary(dictionary_content, blob['name'], metadata=metadata)

@shared_task(name="list_dictionaries")
def list_dictionaries(bucket_name, storage_path):
    """List dictionaries in the bucket."""
    dictionarys_storage = DictionariesStorage(bucket_name, storage_path)
    return dictionarys_storage.list_dictionaries()

@shared_task(name="dictionary_exists")
def dictionary_exists(bucket_name, storage_path, dictionary_name):
    """Check if a dictionary exists in the bucket."""
    dictionarys_storage = DictionariesStorage(bucket_name, storage_path)
    return dictionarys_storage.exists_dictionary(dictionary_name)