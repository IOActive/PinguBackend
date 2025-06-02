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
from PinguApi.submodels.job import Job
from PinguApi.submodels.testcase import TestCase
import uuid
from PinguApi.submodels.platforms import Supported_Platforms
class TestcaseVariantStatus(models.Choices):
    PENDING = 0
    REPRODUCIBLE = 1
    FLAKY = 2
    UNREPRODUCIBLE = 3
        
class TestCaseVariant(models.Model):
    
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Status of the testcase variant (pending, reproducible, unreproducible, etc).
    status = models.IntegerField(
        choices=TestcaseVariantStatus.choices,
        default=TestcaseVariantStatus.PENDING,
    )

    # References
    testcase = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE)

    # Revision that the testcase variant was tried against.
    revision = models.IntegerField(default=1)

    # Crash type.
    crash_type = models.CharField(max_length=50, default="")

    # Crash state.
    crash_state = models.CharField(max_length=50, default="")

    # Bool to indicate if it is a security bug?
    security_flag = models.BooleanField(default=False)

    # Bool to indicate if crash is similar to original testcase.
    is_similar = models.BooleanField(default=False)

    # Similar testcase reproducer key (optional). This is set in case we notice a
    # similar crash on another platform.
    reproducer_key = models.CharField(max_length=200, default="")

    # Platform (e.g. windows, linux, android).
    platform = models.CharField(max_length=50,
                                default='NA',
                                choices=Supported_Platforms.choices)
    
    class Meta:
        db_table = 'testcase_variant'
    
