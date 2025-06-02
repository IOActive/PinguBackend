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

class JobTemplate(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    environment_string = models.CharField(max_length=400, null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'name'], name="%(app_label)s_%(class)s_unique")
        ]
        db_table = 'job_template'