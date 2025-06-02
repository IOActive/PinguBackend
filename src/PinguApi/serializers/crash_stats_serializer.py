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
from PinguApi.submodels.crash_stats import CrashStats

 
class CrashStatsSerializer(serializers.ModelSerializer):
   
    fuzzer_id = serializers.UUIDField(source="fuzzer")
    project_id = serializers.UUIDField(source="project")
    job_id = serializers.UUIDField(source="job")
    testcase_id = serializers.UUIDField(source="testcase", required=False, allow_null=True)
    crash_id = serializers.UUIDField(source="crash", required=False, allow_null=True)

    
    class Meta:
        model = CrashStats
        fields = (
            'id',
            'fuzzer_id',
            'project_id',
            'job_id',
            'testcase_id',
            'crash_id',
            'crash_type',
            'crash_state',
            'security_flag',
            'reproducible_flag',
            'revision',
            'new_flag',
            'platform',
            'crash_time_in_ms',
        )