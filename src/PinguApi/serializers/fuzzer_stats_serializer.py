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
from PinguApi.submodels.fuzzer_stats import FuzzerStats
 
 
class FuzzerStatsSerializer(serializers.ModelSerializer):
    
    start_date = serializers.CharField(required=False, help_text="Start date for the filter")
    end_date = serializers.CharField(required=False, help_text="End date for the filter")
    group_by = serializers.CharField(required=False, help_text="Field to group by")
    interval = serializers.CharField(required=False, help_text="Field to select time bucket size")

    class Meta:
        model = FuzzerStats
        fields = ('id', 'fuzz_target', 'start_date', 'end_date', 'group_by', 'interval')