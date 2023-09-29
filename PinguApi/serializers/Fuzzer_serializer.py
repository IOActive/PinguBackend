from rest_framework import serializers 
from PinguApi.submodels.Fuzzer import Fuzzer
from PinguApi.utils.Base64FileField import ZIPBase64File

class FuzzerSerializer(serializers.ModelSerializer):
    
    fuzzer_zip = ZIPBase64File()
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
                  'data_bundle_name'
                  )
        
    def create(self, validated_data):
        # Exclude the fuzzer_zip parameter from the validated data
        validated_data.pop('fuzzer_zip', None)

        # Create the Fuzzer object
        fuzzer = Fuzzer.objects.create(**validated_data)

        return fuzzer