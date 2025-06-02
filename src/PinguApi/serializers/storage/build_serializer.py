from rest_framework import serializers

class BuildSerializer(serializers.Serializer):
    project_id = serializers.CharField(max_length=255, required=True)
    build_type = serializers.ChoiceField(choices=["release", "sym-release", "sym-debug", "stable-build", "beta-build"], required=True)
    file_path = serializers.CharField(max_length=255, required=False, allow_blank=True)
