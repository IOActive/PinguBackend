import datetime
from celery import shared_task
from PinguApi.handlers.big_query import BigQueryHelper
from celery.utils.log import get_task_logger
from django.utils import timezone


logger = get_task_logger(__name__)
             

# Stats Taks 
@shared_task(name="download_and_update_stats")
def download_and_update_stats(since=datetime.datetime.now(timezone.get_current_timezone())):
    # Your periodic task logic here
    # This task will run at the specified interval
    logger.info("Launching Stats syncronization Task")
    helper = BigQueryHelper()
    try:
        helper.update_stats_since_date(date=since)
        logger.info("Stats syncronization Task Completed")
        return True
    except Exception as e:
        logger.error(f"Failed to update stats from {since}")
        raise Exception(f"Failed to update stats from {since}")