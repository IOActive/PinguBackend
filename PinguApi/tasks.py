# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True)
def add_bot_task(self, command, argument, platform, job_id):
    queue = f'tasks-{platform}'
    if not queue_exists(queue):
        create_queue(current_app.config['queue_host'], queue)
        
    task = {'job_id': str(job.id),
            'platform': platform,
            'command': command,
            'argument': argument,
            }
    
    publish(current_app.config['queue_host'], queue, json.dumps(task))
