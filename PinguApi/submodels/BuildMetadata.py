import datetime
from django.db import models
from PinguApi.submodels.Job import Job
import uuid

class BuildMetadata(models.Model):
    """Metadata associated with a particular archived build."""
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Job type that this build belongs to.
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE, default=None, null=True)

    # Revision of the build.
    revision = models.IntegerField(default=1)

    # Good build or bad build.
    bad_build = models.BooleanField(default=False)

    # Stdout and stderr.
    console_output = models.CharField(max_length=20000, blank=True, default='', null=True)

    # Bot name.
    bot_name = models.CharField(max_length=20)

    # Symbol data.
    symbols =  models.CharField(max_length=20000, blank=True, default='', null=True)

    # Creation timestamp.
    timestamp = models.DateField()

