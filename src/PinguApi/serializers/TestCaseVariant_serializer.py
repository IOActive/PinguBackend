from rest_framework import serializers 
from PinguApi.submodels.TestCaseVariant import TestCaseVariant
from PinguApi.submodels.Job import Job
from PinguApi.submodels.TestCase import TestCase
class TestCaseVariantSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Job.objects.all())
    testcase_id = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=TestCase.objects.all())
    
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