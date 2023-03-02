from django.db import models
from PinguApi.submodels.Job import Job
from PinguApi.submodels.TestCase import TestCase

class TestCaseVariant(models.Model):
    
    class TestcaseVariantStatus(models.TextChoices):
        PENDING = 0
        REPRODUCIBLE = 1
        FLAKY = 2
        UNREPRODUCIBLE = 3
        
    # Status of the testcase variant (pending, reproducible, unreproducible, etc).
    status = models.IntegerField(
        choices=TestcaseVariantStatus.choices,
        default=TestcaseVariantStatus.PENDING,
    )

    # References
    testcase_id = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
    job_id = models.ForeignKey(to=Job, on_delete=models.CASCADE)

    # Revision that the testcase variant was tried against.
    revision = models.IntegerField(default=1)

    # Crash type.
    crash_type = models.CharField(max_length=50, default="")

    # Crash state.
    crash_state = models.CharField(max_length=50, default="")

    # Bool to indicate if it is a security bug?
    security_flag = models.BooleanField(default=False)

    # Bool to indicate if crash is similar to original testcase.
    is_similar = models.BooleanField(default=False)

    # Similar testcase reproducer key (optional). This is set in case we notice a
    # similar crash on another platform.
    reproducer_key = models.CharField(max_length=200, default="")

    # Platform (e.g. windows, linux, android).
    platform = models.CharField(max_length=50, default="")
