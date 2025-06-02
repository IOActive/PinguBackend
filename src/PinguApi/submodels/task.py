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

from django.db import models
import uuid

from PinguApi.submodels.platforms import Supported_Platforms
from PinguApi.submodels.job import Job

class Task(models.Model):
    class TaskStatus(models.TextChoices):
        STARTED = 'started'
        WIP = 'in-progress'
        FINISHED = 'finished'
        ERROR = 'errored out'
        NA = 'NA'
    
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Platform (esp important for Android platform for OS version).
    platform = models.CharField(max_length=50,
                                default='NA',
                                choices=Supported_Platforms.choices)
    
    command = models.CharField(max_length=200, default='')
    
    argument = models.CharField(max_length=200, default='')
    
    # Task payload containing information on current task execution.
    payload = models.CharField(max_length=200, blank=True, null=True)

    # Expected end time for task.
    end_time = models.DateTimeField(null=True, blank=True)

    # Create time stamp of the task.
    create_time = models.DateTimeField(auto_now_add=True)

    # Tasks status
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NA,
    )

    # Text file containing the bot logs. Dont store it to the Database just keep the blob data.
    bot_log = models.FileField(upload_to='tmp', null=True, verbose_name="")
    
    heartbeat_log = models.FileField(upload_to='tmp', null=True, verbose_name="")
    
    run_fuzzer_log = models.FileField(upload_to='tmp', null=True, verbose_name="")
    
    run_heartbeat_log = models.FileField(upload_to='tmp', null=True, verbose_name="")
    
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'task'
