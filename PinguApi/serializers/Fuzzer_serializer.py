from rest_framework import serializers 
from PinguApi.submodels.Fuzzer import Fuzzer

class FuzzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuzzer
        fields = ('id',
                  'timestamp',
                  'name',
                  'filename',
                  'file_size',
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
                  'data_bundle_name'
                  )