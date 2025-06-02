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

from drf_extra_fields.fields import Base64FileField
from logging import getLogger


class ZIPBase64File(Base64FileField):
    ALLOWED_TYPES = ['zip']
    
    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'File Content',
            'description': 'Content of the file base64 encoded',
            'read_only': True
        }

    def get_file_extension(self, filename, decoded_file):
        try:
            filename.split('.')[-1]
        except Exception as e:
            getLogger('PinguAPI').info(e)
        else:
            return 'zip'
            
     