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

from rest_framework import serializers 
from PinguApi.submodels.TestCase import TestCase
from PinguApi.submodels.Job import Job
from PinguApi.submodels.Fuzzer import Fuzzer

class TestCaseSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Job.objects.all())
    fuzzer_id = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Fuzzer.objects.all())
    
    class Meta:
        model = TestCase
        fields = ('id',
                  'bug_information',
                  'test_case',
                  'fixed',
                  'one_time_crasher_flag',
                  'comments',
                  'absolute_path',
                  'queue',
                  'archived',
                  'timestamp',
                  'status',
                  'triaged',
                  'has_bug_flag',
                  'open',
                  'testcase_path',
                  'additional_metadata',
                  'fuzzed_keys',
                  'minimized_keys',
                  'minidump_keys',
                  'minimized_arguments',
                  'disable_ubsan',
                  'regression',
                  'timeout_multiplier',
                  'archive_state',
                  'redzone',
                  'job_id',
                  'fuzzer_id'
                  )