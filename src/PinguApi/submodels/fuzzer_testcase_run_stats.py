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
from PinguApi.submodels.fuzzer_stats import FuzzerStats
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager
from django.utils.timezone import now

class FuzzerTestcaseRunStats(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fuzzer_stats = models.ForeignKey(to=FuzzerStats, on_delete=models.CASCADE)
    
    custom_stats = models.JSONField(null=True)
    
    time = TimescaleDateTimeField(interval="1 day",default=now)
    objects = TimescaleManager()
    
    class Meta:
        db_table = 'fuzzer_testcase_run_stats'