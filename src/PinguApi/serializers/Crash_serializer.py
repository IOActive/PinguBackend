from rest_framework import serializers 
from PinguApi.submodels.Crash import Crash
from PinguApi.submodels.TestCase import TestCase
class CrashSerializer(serializers.ModelSerializer):
    testcase_id = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=TestCase.objects.all())
    class Meta:
        model = Crash
        fields = (  "id",
                    "testcase_id",
                    "crash_signal",
                    "exploitability",
                    "crash_time",
                    "crash_hash",
                    "verified",
                    "additional",
                    "iteration",
                    "crash_type",
                    "crash_address",
                    "crash_state",
                    "crash_stacktrace",
                    "regression",
                    "security_severity",
                    "absolute_path",
                    "security_flag",
                    "reproducible_flag",
                    "return_code",
                    "gestures",
                    "resource_list",
                    "fuzzing_strategy",
                    "should_be_ignored",
                    "application_command_line",
                    "unsymbolized_crash_stacktrace",
                    "crash_frame",
                    "crash_info",
                    "crash_revision"
                )