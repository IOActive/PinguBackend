from django.db import models
from PinguApi.submodels.FuzzTarget import FuzzTarget
from PinguApi.submodels.Job import Job
from PinguApi.submodels.Fuzzer import Fuzzer
import uuid

class FuzzTargetJob(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fully qualified fuzz target name.
    fuzzing_target = models.ForeignKey(to=FuzzTarget, on_delete=models.CASCADE, blank=True, null=True, default=None)

    # Job this target ran as.
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE, blank=True, null=True, default=None)

    # Engine this ran as.
    engine = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE, blank=True, null=True, default=None)

    # Relative frequency with which to select this fuzzer.
    weight = models.FloatField(default=1.0)

    # Approximate last time this target was run.
    last_run = models.DateField()
