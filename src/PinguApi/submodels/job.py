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
from PinguApi.submodels.project import Project
from PinguApi.submodels.Job_template import JobTemplate
class Job(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Job type name.
    name = models.CharField(max_length=50)
    # Description of the job.
    description = models.CharField(max_length=400)
    # Project from the Job belongs.
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    # Creation date
    date = models.DateTimeField()
    # Enable state
    enabled = models.BooleanField(default=True)
    # Archive state
    archived = models.BooleanField(default=False)
    # Job Owner
    #owner = ReferenceField(User, blank=True, null=True, default=None)
    # The platform that this job can run on.
    platform = models.CharField(max_length=50,
                                default='NA',
                                choices=Supported_Platforms.choices)
    
    # Job environment string.
    environment_string = models.CharField(max_length=2000, blank=True, null=False, default="CUSTOM_BINARY=false")
    # Template to use, if any.
    template = models.ForeignKey(to=JobTemplate, on_delete=models.CASCADE, blank=True, null=True, default=None)
    # Blobstore key of the custom binary for this job.
    custom_binary_key = models.CharField(max_length=50, blank=True, null=True, default="")
    # Blobstore path of the custom binary for this job.
    custom_binary_path = models.CharField(max_length=500, blank=True, null=True, default="")
    # Filename for the custom binary.
    custom_binary_filename = models.CharField(max_length=50, blank=True, null=True, default="")
    # Revision of the custom binary.
    custom_binary_revision = models.IntegerField(blank=True, null=True, default=1)
    
    class Meta:
        db_table = 'job'