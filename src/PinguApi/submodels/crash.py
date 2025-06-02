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
from PinguApi.submodels.testcase import TestCase
import uuid

class Crash(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    testcase = models.ForeignKey(to=TestCase, on_delete=models.CASCADE, related_name='crash_testcase')
    crash_signal = models.IntegerField()
    exploitability = models.CharField(max_length=50, blank=True, null=True)
    crash_time = models.IntegerField()
    crash_hash = models.CharField(max_length=512)
    verified = models.BooleanField(default=False)
    additional  = models.TextField(blank=True, null=True)
    iteration = models.IntegerField()
    crash_type = models.CharField(max_length=50)
    crash_address = models.CharField(max_length=50, blank=True, null=True)
    crash_state = models.TextField()
    crash_stacktrace = models.TextField()
    security_severity = models.IntegerField(null=True, blank=True)
    absolute_path = models.TextField()
    security_flag = models.BooleanField()
    reproducible_flag = models.BooleanField(default=False)
    return_code = models.CharField(max_length=50)
    gestures = models.JSONField(null=True)
    resource_list = models.JSONField(null=True)
    fuzzing_strategy = models.JSONField()
    should_be_ignored = models.BooleanField(default=False)
    application_command_line = models.TextField(blank=True, null=True)
    unsymbolized_crash_stacktrace = models.TextField()
    crash_frame = models.JSONField(null=True)
    crash_info = models.CharField(max_length=200, null=True, blank=True)
    crash_revision = models.IntegerField(default=1)
    flaky_stack = models.BooleanField(default=False, null=True)
    
    
    def get_list(self):
        list = ast.literal_eval(self.gestures)
        return list
    
    class Meta:
        db_table = 'crash'