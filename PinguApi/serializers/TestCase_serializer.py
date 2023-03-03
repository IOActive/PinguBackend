from rest_framework import serializers 
from PinguApi.submodels.TestCase import TestCase

class TestCaseSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    fuzzer_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = TestCase
        fields = ('id',
                  'bug_information',
                  'test_case',
                  'fixed',
                  'one_time_crasher_flag',
                  'comments',
                  'absolute_path',
                  'queue',
                  'archived',
                  'timestamp',
                  'status',
                  'triaged',
                  'has_bug_flag',
                  'opened',
                  'testcase_path',
                  'additional_metadata',
                  'fuzzed_keys',
                  'minimized_keys',
                  'minidump_keys',
                  'minimized_arguments',
                  'disable_ubsan',
                  'regression',
                  'timeout_multiplier',
                  'archive_state',
                  'redzone',
                  'job_id',
                  'fuzzer_id'
                  )