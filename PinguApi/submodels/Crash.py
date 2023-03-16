from django.db import models
from PinguApi.submodels.TestCase import TestCase
import uuid

class Crash(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    testcase_id = models.ForeignKey(to=TestCase, on_delete=models.CASCADE, related_name='crash_testcase')
    crash_signal = models.IntegerField()
    exploitability = models.CharField(max_length=50, blank=True, null=True)
    crash_time = models.DateTimeField()
    crash_hash = models.CharField(max_length=512)
    verified = models.BooleanField(default=False)
    additional  = models.CharField(max_length=200, blank=True, null=True)
    iteration = models.IntegerField()
    crash_type = models.CharField(max_length=50)
    crash_address = models.CharField(max_length=50, blank=True, null=True)
    crash_state = models.CharField(max_length=200)
    crash_stacktrace = models.CharField(max_length=20000)
    regression = models.CharField(max_length=200)
    security_severity = models.IntegerField()
    absolute_path = models.CharField(max_length=500)
    security_flag = models.BooleanField()
    reproducible_flag = models.BooleanField(default=False)
    return_code = models.CharField(max_length=50)
    gestures = models.JSONField(null=True)
    resource_list = models.JSONField(null=True)
    fuzzing_strategy = models.JSONField()
    should_be_ignored = models.BooleanField(default=False)
    application_command_line = models.CharField(max_length=200, blank=True, null=True)
    unsymbolized_crash_stacktrace = models.CharField(max_length=20000)
    crash_frame = models.JSONField(null=True)
    crash_info = models.CharField(max_length=200, null=True, blank=True)
    crash_revision = models.IntegerField(default=1)
    
    
    def get_list(self):
        list = ast.literal_eval(self.gestures)
        return list