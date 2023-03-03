from enum import Enum

from django.db import models
from PinguApi.submodels.Job import Job
from PinguApi.submodels.Fuzzer import Fuzzer


class TestCase(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        ONGOING = 'processed'
        UNREPRODUCIBLE = 'unreproducible'
        DONE = 'done'
        
    bug_information = models.CharField(max_length=500)

    # Testcase file
    test_case = models.BinaryField()
    fixed = models.BooleanField(default=False)

    # Did the bug only reproduced once ?
    one_time_crasher_flag = models.BooleanField(default=False)
    comments = models.CharField(max_length=500)
    # The file on the bot that generated the testcase.
    absolute_path = models.CharField(max_length=200)
    # Queue to publish tasks
    queue = models.CharField(max_length=50)
    archived = models.BooleanField(default=False)
    timestamp = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    # indicating if cleanup triage needs to be done.
    triaged = models.BooleanField(default=False)
    # Whether testcase has a bug (either bug_information or group_bug_information).
    has_bug_flag = models.BooleanField(default=False)
    opened = models.BooleanField(default=True)

    # store paths for various things like original testcase, minimized
    # testcase, etc.
    testcase_path = models.CharField(max_length=200)
    additional_metadata = models.CharField(max_length=500)

    # Blobstore keys for various things like original testcase, minimized
    # testcase, etc.
    fuzzed_keys = models.CharField(max_length=200)
    minimized_keys = models.CharField(max_length=200)
    minidump_keys = models.CharField(max_length=200)

    # Minimized argument list.
    minimized_arguments = models.CharField(max_length=200)

    # Flag indicating if UBSan detection should be disabled. This is needed for
    # cases when ASan and UBSan are bundled in the same build configuration
    # and we need to disable UBSan in some runs to find the potentially more
    # interesting ASan bugs.
    disable_ubsan = models.BooleanField(default=False)

    # Regression range.
    regression = models.CharField(max_length=200)

    # Adjusts timeout based on multiplier value.
    timeout_multiplier = models.FloatField(default=1.0)

    # State representing whether the fuzzed or minimized testcases are archived.
    archive_state = models.IntegerField()

    # ASAN redzone size in bytes.
    redzone =  models.IntegerField(default=128)

    # References
    job_id = models.ForeignKey(to=Job, on_delete=models.CASCADE)
    fuzzer_id = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE)
