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

from PinguApi.submodels.project import Project

class Supported_Builds(models.TextChoices):
        RELEASE = 'Release'
        SYM_RELEASE = 'SYM_Release'
        SYM_DEBUG = 'SYM_Debug'
        STABLE = 'Stable'
        BETA = 'Beta'
        NA = 'NA'

class Build(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Type of build
    type = models.CharField(max_length=50,
                                default='NA',
                                choices=Supported_Builds.choices)
 
    # Zip file containing the build. Dont store it to the Database just keep the blob data.
    build_zip = models.FileField(upload_to='tmp', null=True, verbose_name="")
    
    # Build file name
    filename = models.CharField(max_length=50, default="")

    # String representation of the file size.
    file_size = models.IntegerField(default=0)
    
    # Creation time stamp
    timestamp = models.DateTimeField(auto_now=True)
    
    # Blobstore path or URL for this Build.
    blobstore_path = models.CharField(max_length=200, default="", blank=True, null=True)
    
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'filename'], name="%(app_label)s_%(class)s_unique")
        ]
        db_table = 'build'