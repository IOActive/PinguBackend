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
class Trial(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # App name that this trial is applied to. E.g. "d8" or "chrome".
    app_name = models.CharField(max_length=50)

    # Chance to select this set of arguments. Zero to one.
    probability = models.FloatField(default=1.0)

    # Additional arguments to apply if selected.
    app_args = models.CharField(max_length=200, default="")
