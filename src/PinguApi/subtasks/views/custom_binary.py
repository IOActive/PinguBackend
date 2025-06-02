# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Create your tasks here
import base64
import os
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
import io
from PinguApi.handlers.storage_handlers.blobs import BlobsStorage

logger = get_task_logger(__name__)
             
            
# Custom Binary tasks        
@shared_task(name="upload_custom_binary_to_bucket")
def upload_custom_binary_to_bucket(file,  bucket_name):
    try:
        custom_binary_storage = BlobsStorage(bucket_name=bucket_name)
        file_content = base64.b64decode(file["content"])
              
        custom_binary_storage.write_blob(file_content, file["name"]) 
        logger.info("upload_custom_binary_to_bucket: Custom binary uploaded successfully with key: %s", file["name"])
        
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_custom_binary_from_bucket")
def download_custom_binary_from_bucket(blob_key, bucket_name):
    try:
        custom_binary_storage = BlobsStorage(bucket_name=bucket_name)
    
        if not os.path.exists(custom_binary_storage.cache_path):
            os.makedirs(os.path.dirname(custom_binary_storage.cache_path), exist_ok=True)
    
        custom_binary_storage.read_blob_to_disk(blob_key)
    
        # Step 3: Create an in-memory file
        with (open(f"{custom_binary_storage.cache_path}/{blob_key}", 'rb')) as f:
            return io.BytesIO(f.read())
        
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_custom_binary_from_bucket")
def remove_custom_binary_from_bucket(blob_key, bucket_name):
    try:
        custom_binary_storage = BlobsStorage(bucket_name=bucket_name)
        custom_binary_storage.remove_blob(blob_key)
        logger.info("remove_custom_binary_from_bucket: Custom binary removed successfully")
    except Exception as e:
        logger.error(e)