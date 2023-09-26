# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(name="upload_fuzzer_to_bucket")
def upload_fuzzer_to_bucket(zip_file):
    logger.info("upload_fuzzer_to_bucket")
    return True
