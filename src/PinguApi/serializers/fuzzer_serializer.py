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
from PinguApi.submodels.fuzzer import Fuzzer
from PinguApi.submodels.project import Project
from django.db.models.fields.files import FileField

from django.db.models.fields import TextField

class FuzzerSerializer(serializers.ModelSerializer):
    
    project_id = serializers.PrimaryKeyRelatedField(source='project', many=False, required=False, allow_null=True, queryset=Project.objects.all())
    fuzzer_zip = FileField(null=True)
    download_url = serializers.SerializerMethodField()  # Define as a custom field
    class Meta:
        model = Fuzzer
        fields = ('id',
                  'timestamp',
                  'name',
                  'filename',
                  'file_size',
                  'fuzzer_zip',
                  'blobstore_path',
                  'executable_path',
                  'revision',
                  'timeout',
                  'supported_platforms',
                  'launcher_script',
                  'result',
                  'result_timestamp',
                  'console_output',
                  'return_code',
                  'sample_testcase',
                  'max_testcases',
                  'untrusted_content',
                  'additional_environment_string',
                  'stats_columns',
                  'stats_column_descriptions',
                  'builtin',
                  'differential',
                  'has_large_testcases',
                  'data_bundle_name',
                  'install_script',
                  'project_id',
                  'download_url'
                  )
        
    def create(self, validated_data):
        # Exclude the fuzzer_zip parameter from the validated data
        validated_data.pop('fuzzer_zip', None)

        # Create the Fuzzer object
        fuzzer = Fuzzer.objects.create(**validated_data)

        return fuzzer
    
    def get_download_url(self, obj):
        # Custom method to return the download_url value
        return getattr(obj, 'download_url', None)