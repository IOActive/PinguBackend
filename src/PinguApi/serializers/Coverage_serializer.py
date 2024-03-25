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
from PinguApi.submodels.TestCase import TestCase
from PinguApi.submodels.Coverage import Coverage
class CoverageSerializer(serializers.ModelSerializer):
    testcase = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=TestCase.objects.all())

    class Meta:
        model = Coverage
        fields = ('id',
                  'date',
                  'fuzzer',
                  'functions_covered',
                  'functions_total',
                  'edges_covered',
                  'edges_total',
                  'corpus_size_units',
                  'corpus_size_bytes',
                  'corpus_location',
                  'corpus_backup_location',
                  'quarantine_size_units',
                  'quarantine_size_bytes',
                  'quarantine_location',
                  'html_report_url',
                  'testcase'
                  )