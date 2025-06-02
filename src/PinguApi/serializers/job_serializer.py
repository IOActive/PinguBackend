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
from PinguApi.submodels.job import Job
from PinguApi.submodels.Job_template import JobTemplate
from PinguApi.submodels.project import Project
class JobSerializer(serializers.ModelSerializer):
    template_id = serializers.PrimaryKeyRelatedField(source='template', many=False, required=False, queryset=JobTemplate.objects.all())
    project_id = serializers.PrimaryKeyRelatedField(source='project', many=False, required=False, queryset=Project.objects.all())

    class Meta:
        model = Job
        fields = ('id',
                  'name',
                  'description',
                  'template_id',
                  'date',
                  'enabled',
                  'archived',
                  'platform',
                  'environment_string',
                  'project_id',
                  'custom_binary_path',
                  'custom_binary_filename',
                  'custom_binary_revision',
                  'custom_binary_key',
                  )