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
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.job import Job
from PinguApi.submodels.fuzzer import Fuzzer
import uuid

class FuzzTargetJob(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fully qualified fuzz target name.
    fuzz_target = models.ForeignKey(to=FuzzTarget, on_delete=models.CASCADE)

    # Job this target ran as.
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE, null=False)

    # Engine this ran as.
    fuzzer = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE)

    # Relative frequency with which to select this fuzzer.
    weight = models.FloatField(default=1.0)

    # Approximate last time this target was run.
    last_run = models.DateTimeField()
    
    class Meta:
        db_table = 'fuzzer_target_job'
