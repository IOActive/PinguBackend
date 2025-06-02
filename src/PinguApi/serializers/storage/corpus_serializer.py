from enum import Enum
from rest_framework import serializers

class CorpusTypes(Enum):
    CORPUS = "corpus"
    BACKUP = "backup"
    SHARED = "shared"
    QUARANTINE = "quarantine"

class CorpusUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )
    project_id = serializers.CharField(required=True)
    fuzz_target_id = serializers.CharField(required=True)
    kind = serializers.ChoiceField(required=True, choices=[kind.value for kind in CorpusTypes])