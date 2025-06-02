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
from PinguApi.submodels.testcase_variant import TestCaseVariant
from PinguApi.submodels.job import Job
from PinguApi.submodels.testcase import TestCase
class TestCaseVariantSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(source='job', many=False, required=True, queryset=Job.objects.all())
    testcase_id = serializers.PrimaryKeyRelatedField(source='testcase', many=False, required=True, queryset=TestCase.objects.all())
    
    class Meta:
        model = TestCaseVariant
        fields = ('id',
                  'status',
                  'testcase_id',
                  'job_id',
                  'revision',
                  'crash_type',
                  'crash_state',
                  'security_flag',
                  'is_similar',
                  'reproducer_key',
                  'platform'
                  )