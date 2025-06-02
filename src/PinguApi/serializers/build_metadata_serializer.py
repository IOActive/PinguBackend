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
from PinguApi.submodels.build_metadata import BuildMetadata
 
 
class BuildMetadataSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(source='job', many=False, read_only=True)
    class Meta:
        model = BuildMetadata
        fields = ('id',
                  'job_id',
                  'revision',
                  'bad_build',
                  'console_output',
                  'bot_name',
                  'symbols',
                  'timestamp'
                  )