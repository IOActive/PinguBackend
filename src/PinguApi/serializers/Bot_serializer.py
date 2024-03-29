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
from PinguApi.submodels.Bot import Bot
from PinguApi.utils.Base64FileField import Base64FileField

 
class BotSerializer(serializers.ModelSerializer):

    bot_logs = Base64FileField()
    class Meta:
        model = Bot
        fields = ('id',
                  'name',
                  'last_beat_time',
                  'task_payload',
                  'task_end_time',
                  'task_status',
                  'platform',
                  'blobstore_log_path',
                  'bot_logs',
                  )
