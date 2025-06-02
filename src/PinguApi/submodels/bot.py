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
from PinguApi.submodels.task import Task
class Bot(models.Model):
   
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """Bot health metadata."""
    # Name of the bot.
    name = models.CharField(max_length=40, unique=True)

    # Time of the last heartbeat.
    last_beat_time = models.DateTimeField(null=True, blank=True)

    # Platform (esp important for Android platform for OS version).
    platform = models.CharField(max_length=50,
                                default='NA',
                                choices=Supported_Platforms.choices)

    # forieng key to current Task
    current_task = models.ForeignKey(to=Task, on_delete=models.CASCADE, blank=True, null=True, default=None)
    
    class Meta:
        db_table = 'bot'
    
