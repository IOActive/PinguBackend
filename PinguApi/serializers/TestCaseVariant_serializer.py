from rest_framework import serializers 
from PinguApi.submodels.TestCaseVariant import TestCaseVariant

class TestCaseVariantSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    testcase_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = TestCaseVariant
        fields = ('id',
                  'status',
                  'testcase_id',
                  'job_id',
                  'revision',
                  'crash_type',
                  'crash_state',
                  'security_flag',
                  'is_similar',
                  'reproducer_key',
                  'platform'
                  )