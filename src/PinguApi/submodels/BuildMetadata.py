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

import datetime
from django.db import models
from PinguApi.submodels.Job import Job
import uuid

class BuildMetadata(models.Model):
    """Metadata associated with a particular archived build."""
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Job type that this build belongs to.
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE, default=None, null=True)

    # Revision of the build.
    revision = models.IntegerField(default=1)

    # Good build or bad build.
    bad_build = models.BooleanField(default=False)

    # Stdout and stderr.
    console_output = models.CharField(max_length=20000, blank=True, default='', null=True)

    # Bot name.
    bot_name = models.CharField(max_length=20)

    # Symbol data.
    symbols =  models.CharField(max_length=20000, blank=True, default='', null=True)

    # Creation timestamp.
    timestamp = models.DateTimeField()

