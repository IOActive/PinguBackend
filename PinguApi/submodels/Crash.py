from django.db import models
from PinguApi.submodels.TestCase import TestCase
import uuid

class Crash(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    testcase_id = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
    crash_signal = models.IntegerField()
    exploitability = models.CharField(max_length=50)
    crash_time = models.DateField()
    crash_hash = models.CharField(max_length=512)
    verified = models.BooleanField(default=False)
    additional  = models.CharField(max_length=200)
    iteration = models.IntegerField()
    crash_type = models.CharField(max_length=50)
    crash_address = models.CharField(max_length=50)
    crash_state = models.CharField(max_length=50)
    crash_stacktrace = models.BinaryField()
    regression = models.CharField(max_length=200)
    security_severity = models.IntegerField()
    absolute_path = models.CharField(max_length=50)
    security_flag = models.BooleanField(default=False)
    reproducible_flag = models.BooleanField(default=False)
    return_code = models.CharField(max_length=50)
    gestures = models.JSONField()
    resource_list = models.JSONField()
    fuzzing_strategy = models.JSONField()
    should_be_ignored = models.BooleanField(default=False)
    application_command_line = models.CharField(max_length=200)
    unsymbolized_crash_stacktrace = models.BinaryField()
    crash_frame = models.JSONField()
    crash_info = models.CharField(max_length=200)
    crash_revision = models.IntegerField(default=1)
    
    
    def get_list(self):
        list = ast.literal_eval(self.gestures)
        return list