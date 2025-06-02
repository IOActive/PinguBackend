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
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager
from django.utils.timezone import now
from PinguApi.submodels.platforms import Supported_Platforms

class CrashStats(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Id references to primary models
    fuzzer = models.UUIDField(null=False, blank=False)
    job = models.UUIDField(null=False, blank=False)
    project = models.UUIDField(null=False, blank=False)
    crash = models.UUIDField(null=True, blank=True)
    testcase = models.UUIDField(null=True, blank=True)
    
    # Stats paramers
    crash_type = models.TextField(max_length=50)
    crash_state = models.TextField()
    security_flag = models.BooleanField()
    reproducible_flag = models.BooleanField(default=False)
    revision = models.IntegerField(default=1)
    new_flag = models.BooleanField(default=False)
    platform = models.CharField(
        max_length=50,
        default='NA',
        choices=Supported_Platforms.choices)
    crash_time_in_ms = models.IntegerField(default=0)
    
    time = TimescaleDateTimeField(interval="1 day",default=now)
    objects = TimescaleManager()
    
    class Meta:
        db_table = 'crash_stats'