from enum import Enum
from rest_framework import serializers

class CoverageUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )
    project_id = serializers.CharField(required=True)
    fuzz_target_id = serializers.CharField(required=True)