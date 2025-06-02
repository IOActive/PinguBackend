from rest_framework import serializers

class FuzzerLogsSerializer(serializers.Serializer):
    log_type = serializers.ChoiceField(choices=["bot", "fuzzer"], required=True)
    job_id = serializers.CharField(max_length=255, required=True)
    fuzzer_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    project_id = serializers.CharField(max_length=255, required=True)
    date = serializers.DateTimeField(required=False, allow_null=True)
    files = serializers.ListField(
        required=False,
        child=serializers.FileField(required=False, allow_empty_file=True),
        allow_empty=True
    )

class BotLogsSerializer(serializers.Serializer):
    log_type = serializers.ChoiceField(choices=["bot"], required=True)
    task_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    project_id = serializers.CharField(max_length=255, required=True)
    job_id = serializers.CharField(max_length=255, required=True)
    files = serializers.ListField(
        required=False,
        child=serializers.FileField(required=False, allow_empty_file=True),
        allow_empty=True,
        
    )
