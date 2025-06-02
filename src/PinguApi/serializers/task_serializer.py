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
from PinguApi.submodels.task import Task
from src.PinguApi.utilities.base64_file_field import Base64FileField
from PinguApi.submodels.job import Job

class TaskSerializer(serializers.ModelSerializer):
    
    bot_log = Base64FileField()
    heartbeat_log = Base64FileField()
    run_fuzzer_log = Base64FileField()
    run_heartbeat_log = Base64FileField()
    job_id = serializers.PrimaryKeyRelatedField(source='job', many=False, required=False, queryset=Job.objects.all())


    class Meta:
        model = Task
        fields = ['id',
                  'platform',
                  'command',
                  'argument',
                  'payload',
                  'end_time',
                  'create_time',
                  'status',
                  'bot_log', 
                  'heartbeat_log', 
                  'run_fuzzer_log', 
                  'run_heartbeat_log', 
                  #'blobstore_log_path',
                  'job_id']