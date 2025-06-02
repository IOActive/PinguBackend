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
from PinguApi.submodels.fuzzer import Fuzzer
import uuid

from PinguApi.submodels.project import Project


class FuzzTarget(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Selected Fuzzer
    fuzzer = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE)
    # Target File
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    # Binary name.
    binary = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'fuzzer_target'

