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
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from PinguApi.utils.MinioManager import MinioManger
import zipfile
import io
import os
from PinguApi.submodels.Build import Supported_Builds

logger = get_task_logger(__name__)

# Bot Logs Tasks
@shared_task(name="download_bot_logs")
def download_bot_logs(bot_id):
    try:
        bucket_client = MinioManger()
        # get the rest of the path
        result = bucket_client.get_object(bucketName=os.environ.get("BOT_LOGS_BUCKET"), fileName=f'{bot_id}/bot.log')
        logger.info("download_fuzzer_from_bucket")
        if result.data:
            return result.data
        else:
            return b'/Empty'
    except Exception as e:
        logger.error(e)

# Fuzzer Tasks
@shared_task(name="upload_fuzzer_to_bucket")
def upload_fuzzer_to_bucket(zip_file_stream, zip_filename):
    try:
        file_stream = io.BytesIO(zip_file_stream)
        size_in_bytes = len(file_stream.getbuffer())
        
        bucket_client = MinioManger()
        result = bucket_client.put_object(bucketName=os.environ.get('FUZZERS_BUCKET'), name=zip_filename, data=file_stream, size=size_in_bytes)
        logger.info("upload_fuzzer_to_bucket")
        blobstore_path = f"{result.bucket_name}/{result.object_name}"
        
        return blobstore_path, size_in_bytes
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_fuzzer_from_bucket")
def download_fuzzer_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.get_object(bucketName=bucket_name, fileName=fileName)
        logger.info("download_fuzzer_from_bucket")
        return result.data
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_fuzzer_from_bucket")
def remove_fuzzer_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.remove_object(bucketName=bucket_name, fileName=fileName)
        logger.info("remove_fuzzer_from_bucket")
        return result
    except Exception as e:
        logger.error(e)

# Builds Tasks
@shared_task(name="upload_build_to_bucket")
def upload_build_to_bucket(zip_file_stream, zip_filename, build_type):
    try:
        file_stream = io.BytesIO(zip_file_stream)
        size_in_bytes = len(file_stream.getbuffer())
        bucketName = ""
        match build_type:
            case Supported_Builds.RELEASE.value:
                bucketName = os.environ.get("RELEASE_BUILD_BUCKET")
            case Supported_Builds.SYM_RELEASE.value:
                bucketName = os.environ.get("SYM_RELEASE_BUILD_BUCKET")
            case Supported_Builds.SYM_DEBUG.value:
                bucketName = os.environ.get("SYM_DEBUG_BUILD_BUCKET")
            case Supported_Builds.STABLE.value:
                bucketName = os.environ.get("STABLE_BUILD_BUCKET")
            case Supported_Builds.BETA.value:
                bucketName = os.environ.get("BETA_BUILD_BUCKET")
            case _:
                bucketName = os.environ.get("RELEASE_BUILD_BUCKET")
                     
        bucket_client = MinioManger()
        result = bucket_client.put_object(bucketName=bucketName, name=zip_filename, data=file_stream, size=size_in_bytes)
        logger.info("upload_build_to_bucket")
        blobstore_path = f"{result.bucket_name}/{result.object_name}"
        
        return blobstore_path, size_in_bytes
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_build_from_bucket")
def download_build_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.get_object(bucketName=bucket_name, fileName=fileName)
        logger.info("download_build_from_bucket")
        return result.data
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_build_from_bucket")
def remove_build_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.remove_object(bucketName=bucket_name, fileName=fileName)
        logger.info("remove_build_from_bucket")
        return result
    except Exception as e:
        logger.error(e)
        
        
            
# Custom Binary tasks        
@shared_task(name="upload_custom_binary_to_bucket")
def upload_custom_binary_to_bucket(zip_file_stream, zip_filename):
    try:
        file_stream = io.BytesIO(zip_file_stream)
        size_in_bytes = len(file_stream.getbuffer())
        
        bucket_client = MinioManger()
        result = bucket_client.put_object(bucketName=os.environ.get('BLOBS_BUCKET'), name=zip_filename, data=file_stream, size=size_in_bytes)
        logger.info("upload_custom_binary_to_bucket")
        blobstore_path = f"{result.bucket_name}/{result.object_name}"
        
        return blobstore_path, size_in_bytes
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_custom_binary_from_bucket")
def download_custom_binary_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.get_object(bucketName=bucket_name, fileName=fileName)
        logger.info("download_custom_binary_from_bucket")
        return result.data
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_custom_binary_from_bucket")
def remove_custom_binary_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.remove_object(bucketName=bucket_name, fileName=fileName)
        logger.info("remove_custom_binary_from_bucket")
        return result
    except Exception as e:
        logger.error(e)
      
# Corpus Tasks    
@shared_task(name="upload_corpus_to_bucket")
def upload_corpus_to_bucket(zip_file_stream, project_name, fuzzzer_name, fuzztarget_name):
    try:
        zip_file_stream_bytes = io.BytesIO(zip_file_stream)
        bucket_client = MinioManger()

        with zipfile.ZipFile(zip_file_stream_bytes) as zf:
            for file in zf.infolist():
                file_stream_bytes = io.BytesIO(zf.open(file).read())
                size_in_bytes = len(file_stream_bytes.getbuffer())
                file_name = file.filename.split("/")[-1]
                file_path = f"{fuzzzer_name}/{project_name}_{fuzztarget_name}/{file_name}"
                result = bucket_client.put_object(bucketName=os.environ.get('CORPUS_BUCKET'), name=file_path, data=file_stream_bytes, size=size_in_bytes)
                logger.info("upload_corpus_to_bucket")
                blobstore_path = f"{result.bucket_name}/{result.object_name}"
        
        return blobstore_path, size_in_bytes
    except Exception as e:
        logger.error(e)
           
@shared_task(name="download_corpus_from_bucket")
def download_corpus_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.get_object(bucketName=bucket_name, fileName=fileName)
        logger.info("download_corpus_from_bucket")
        return result.data
    except Exception as e:
        logger.error(e)
        
@shared_task(name="remove_corpus_from_bucket")
def remove_corpus_from_bucket(blobstore_path):
    try:
        bucket_client = MinioManger()
        # get the root directory and the rest of the path in two new strings
        splitted_path = blobstore_path.split('/', 1)
        bucket_name = splitted_path[0]
        # get the rest of the path
        fileName = splitted_path[1]
        # get the file from the bucket
        result = bucket_client.remove_object(bucketName=bucket_name, fileName=fileName)
        logger.info("remove_corpus_from_bucket")
        return result
    except Exception as e:
        logger.error(e)
        