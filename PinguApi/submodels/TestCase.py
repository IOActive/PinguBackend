from enum import Enum

from django.db import models
from PinguApi.submodels.Job import Job
from PinguApi.submodels.Fuzzer import Fuzzer
import uuid


class TestCase(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        ONGOING = 'processed'
        UNREPRODUCIBLE = 'unreproducible'
        DONE = 'done'
    
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    bug_information = models.CharField(max_length=500, blank=True, null=True)

    # Testcase file
    test_case = models.BinaryField()
    fixed = models.CharField(max_length=50, blank=True)

    # Did the bug only reproduced once ?
    one_time_crasher_flag = models.BooleanField(default=False)
    comments = models.CharField(max_length=500, blank=True)
    # The file on the bot that generated the testcase.
    absolute_path = models.CharField(max_length=200)
    # Queue to publish tasks
    queue = models.CharField(max_length=50)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    # indicating if cleanup triage needs to be done.
    triaged = models.BooleanField(default=False)
    # Whether testcase has a bug (either bug_information or group_bug_information).
    has_bug_flag = models.BooleanField(default=False)
    open = models.BooleanField(default=True)

    # store paths for various things like original testcase, minimized
    # testcase, etc.
    testcase_path = models.CharField(max_length=200)
    additional_metadata = models.CharField(max_length=500, blank=True)

    # Blobstore keys for various things like original testcase, minimized
    # testcase, etc.
    fuzzed_keys = models.CharField(max_length=200, blank=True, null=True)
    minimized_keys = models.CharField(max_length=200, blank=True, null=True)
    minidump_keys = models.CharField(max_length=200, blank=True, null=True)

    # Minimized argument list.
    minimized_arguments = models.CharField(max_length=200, blank=True, null=True)

    # Flag indicating if UBSan detection should be disabled. This is needed for
    # cases when ASan and UBSan are bundled in the same build configuration
    # and we need to disable UBSan in some runs to find the potentially more
    # interesting ASan bugs.
    disable_ubsan = models.BooleanField(default=False)

    # Regression range.
    regression = models.CharField(max_length=200, blank=True, null=True)

    # Adjusts timeout based on multiplier value.
    timeout_multiplier = models.FloatField(default=1.0)

    # State representing whether the fuzzed or minimized testcases are archived.
    archive_state = models.IntegerField()

    # ASAN redzone size in bytes.
    redzone =  models.IntegerField(default=128)

    # References
    job_id = models.ForeignKey(to=Job, on_delete=models.CASCADE, related_name="testcase_job")
    fuzzer_id = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE)
