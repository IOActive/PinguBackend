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
from PinguApi.submodels.fuzz_target_job import FuzzTargetJob
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.job import Job
from PinguApi.submodels.fuzzer import Fuzzer

class FuzzTargetJobSerializer(serializers.ModelSerializer):
    
    fuzz_target_id = serializers.PrimaryKeyRelatedField(source='fuzz_target', many=False, required=True, queryset=FuzzTarget.objects.all())
    job_id = serializers.PrimaryKeyRelatedField(source='job', many=False, required=True, queryset=Job.objects.all())
    fuzzer_id = serializers.PrimaryKeyRelatedField(source='fuzzer', many=False, required=True, queryset=Fuzzer.objects.all())
    
    class Meta:
        model = FuzzTargetJob
        fields = ('id',
                  'fuzz_target_id',
                  'job_id',
                  'fuzzer_id',
                  'weight',
                  'last_run'
                  )