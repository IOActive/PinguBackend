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
import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from PinguApi.handlers.storage_handlers.logs import LogsStorage

logger = get_task_logger(__name__)

# Bot Logs Tasks
@shared_task(name="download_task_logs")
def download_task_logs(bucket_name, storage_path):
    try:
        logs_storage = LogsStorage(bucket_name=bucket_name, bucket_path=storage_path)
        if not os.path.exists(logs_storage.cache_path):
            os.makedirs(logs_storage.cache_path)
            
        logs_storage.rsync_to_disk()
        
        logs = {
            'bot_log': None,
            'heartbeat_log': None,
            'run_fuzzer_log': None,
            'run_heartbeat_log': None,
        }
        
        cache_logs_path = f"{logs_storage.cache_path}"
        
        for log_file in os.listdir(cache_logs_path):
            if log_file in ('bot.log', 'heartbeat.log', 'run_fuzzer.log', 'run_heartbeat.log'):
                with open(os.path.join(cache_logs_path, log_file), 'rb') as f:
                    file_content = f.read()
                    match log_file:
                        case 'bot.log':
                            logs['bot_log'] = file_content
                        case 'heartbeat.log':
                            logs['heartbeat_log'] = file_content
                        case 'run_fuzzer.log':
                            logs['run_fuzzer_log'] = file_content
                        case 'run_heartbeat.log':
                            logs['run_heartbeat_log'] = file_content
        return logs
    
    except Exception as e:
        logger.error(e)
        return None, None, None, None
