from enum import Enum
from rest_framework import serializers
class StatsKind(Enum):
    TEST_CASE_RUN = "TestcaseRun"
    JOB_RUN = "JobRun"
    
class StatsUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )
    project_id = serializers.CharField(required=True)
    fuzz_target_id = serializers.CharField(required=True)
    job_id = serializers.CharField(required=True)
    kind = serializers.ChoiceField(required=True, choices=[kind.value for kind in StatsKind])