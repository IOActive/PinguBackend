import base64
import io
import os
from celery import shared_task
from celery.utils.log import get_task_logger
from PinguApi.handlers.storage_handlers.corpus import CorpusStorage

logger = get_task_logger(__name__)

# Corpus Tasks    
@shared_task(name="upload_corpus_to_bucket")
def upload_corpus_to_bucket(file, bucket_name, bucket_path):
    
    try:
        corpus_storage = CorpusStorage(bucket_name=bucket_name, bucket_path=bucket_path)
        file_content = base64.b64decode(file["content"])
                     
        corpus_storage.upload_corpus(file_content, file["name"]) 
        
    except Exception as e:
        logger.error(e)
