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
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.fuzzer import Fuzzer
from PinguApi.submodels.project import Project

class FuzzTargetSerializer(serializers.ModelSerializer):
    fuzzer_id = serializers.PrimaryKeyRelatedField(source='fuzzer', many=False, required=True, queryset=Fuzzer.objects.all())
    project_id = serializers.PrimaryKeyRelatedField(source='project', many=False, required=True, queryset=Project.objects.all())

    class Meta:
        model = FuzzTarget
        fields = ('id',
                  'fuzzer_id',
                  'project_id',
                  'binary'
                  )