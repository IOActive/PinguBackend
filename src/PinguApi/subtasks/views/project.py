# Project Tasks
from celery import shared_task
from minio import S3Error

from PinguApi.handlers import storage
# Create your tasks here
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task(name="create_project_buckets")
def create_project_buckets(buckets):
    for bucket_name in buckets:
        try:
            storage.create_bucket_if_needed(bucket_name)
            logger.info("Bucket created")
        except S3Error as e:
            if e.code == 'BucketAlreadyOwnedByYou':
                logger.info("Bucket already exists")
                continue
            return False 
        except Exception as e:
            logger.error(e)
            return False
    return True

@shared_task(name="delete_project_buckets")
def delete_project_buckets(buckets):
    for bucket_name in buckets:
        try:
            storage.delete_bucket(bucket_name)
            logger.info(f"Bucket deleted {bucket_name}")
        except Exception as e:
            logger.error(e)
            continue
    return True