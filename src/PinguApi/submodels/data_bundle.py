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

class DataBundle(models.Model):
    VALID_NAME_REGEX = models.CharField(max_length=100, blank=True, null=True, default="")
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The data bundle's name (important for identifying shared bundles).
    name = models.CharField(max_length=50)

    # Name of cloud storage bucket on GCS.
    bucket_name = models.CharField(max_length=50)

    # Data bundle's source (for accountability).
    source = models.CharField(max_length=50, blank=True, null=True, default="")

    # If data bundle can be unpacked locally or needs nfs.
    is_local = models.BooleanField(default=True)

    # Creation timestamp.
    timestamp = models.DateTimeField()

    # Whether or not bundle should be synced to worker instead.
    # Fuzzer scripts are usually run on trusted hosts, so data bundles are synced
    # there. In libFuzzer's case, we want the bundle to be on the same machine as
    # where the libFuzzer binary will run (untrusted).
    sync_to_worker = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'databundle'
