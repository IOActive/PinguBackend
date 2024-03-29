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
from PinguApi.submodels.TestCase import TestCase
import uuid

class Coverage(models.Model):
    """Coverage info."""
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    fuzzer = models.CharField(max_length=50)

    # Function coverage information.
    functions_covered = models.IntegerField()
    functions_total = models.IntegerField()

    # Edge coverage information.
    edges_covered = models.IntegerField()
    edges_total = models.IntegerField()

    # Corpus size information.
    corpus_size_units = models.IntegerField()
    corpus_size_bytes = models.IntegerField()
    corpus_location = models.CharField(max_length=200)

    # Corpus backup information.
    corpus_backup_location = models.CharField(max_length=200)

    # Quarantine size information.
    quarantine_size_units = models.IntegerField() 
    quarantine_size_bytes = models.IntegerField()
    quarantine_location = models.CharField(max_length=200)

    # Link to the HTML report.
    html_report_url = models.BinaryField()

    # References
    testcase = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
