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
from PinguApi.submodels.Build import Build
from PinguApi.utils.Base64FileField import ZIPBase64File

class BuildSerializer(serializers.ModelSerializer):
    
    build_zip = ZIPBase64File()
    class Meta:
        model = Build
        fields = ('id',
                  'type',
                  'build_zip',
                  'filename',
                  'file_size',
                  'timestamp',
                  'blobstore_path',
                  )
        
    def create(self, validated_data):
        # Exclude the fuzzer_zip parameter from the validated data
        validated_data.pop('build_zip', None)

        # Create the Fuzzer object
        build = Build.objects.create(**validated_data)

        return build