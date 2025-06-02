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
from PinguApi.submodels.crash import Crash
from PinguApi.submodels.testcase import TestCase
class CrashSerializer(serializers.ModelSerializer):
    testcase_id = serializers.PrimaryKeyRelatedField(source='testcase', many=False, required=True, queryset=TestCase.objects.all())
    class Meta:
        model = Crash
        fields = (  "id",
                    "testcase_id",
                    "crash_signal",
                    "exploitability",
                    "crash_time",
                    "crash_hash",
                    "verified",
                    "additional",
                    "iteration",
                    "crash_type",
                    "crash_address",
                    "crash_state",
                    "crash_stacktrace",
                    "security_severity",
                    "absolute_path",
                    "security_flag",
                    "reproducible_flag",
                    "return_code",
                    "gestures",
                    "resource_list",
                    "fuzzing_strategy",
                    "should_be_ignored",
                    "application_command_line",
                    "unsymbolized_crash_stacktrace",
                    "crash_frame",
                    "crash_info",
                    "crash_revision"
                )