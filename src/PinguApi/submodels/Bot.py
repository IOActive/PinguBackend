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

from enum import Enum
from django.db import models
import uuid
from django.conf import settings 
from PinguApi.submodels.Platforms import Supported_Platforms
class Bot(models.Model):
    class TaskStatus(models.TextChoices):
        STARTED = 'started'
        WIP = 'in-progress'
        FINISHED = 'finished'
        ERROR = 'errored out'
        NA = 'NA'
    
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """Bot health metadata."""
    # Name of the bot.
    name = models.CharField(max_length=40, unique=True)

    # Time of the last heartbeat.
    last_beat_time = models.DateTimeField(null=True, blank=True)

    # Task payload containing information on current task execution.
    task_payload = models.CharField(max_length=200, blank=True, null=True)

    # Expected end time for task.
    task_end_time = models.DateTimeField(null=True, blank=True)

    # Tasks status
    task_status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NA,
    )

    # Platform (esp important for Android platform for OS version).
    platform = models.CharField(max_length=50,
                                default='NA',
                                choices=Supported_Platforms.choices)
    
    # Blobstore path or URL for this fuzzer.
    blobstore_log_path = models.CharField(max_length=200, default="", blank=True, null=True)

    # Text file containing the bot logs. Dont store it to the Database just keep the blob data.
    bot_logs = models.FileField(upload_to='tmp', null=True, verbose_name="")
    
