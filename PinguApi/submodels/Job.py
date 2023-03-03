from django.db import models
from PinguApi.submodels.JobTemplate import JobTemplate
import uuid
class Job(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Job type name.
    name = models.CharField(max_length=50)
    # Description of the job.
    description = models.CharField(max_length=400)
    # Project name.
    project = models.CharField(max_length=50)
    # Creation date
    date = models.DateField()
    # Enable state
    enabled = models.BooleanField(default=True)
    # Archive state
    archived = models.BooleanField(default=False)
    # Job Owner
    #owner = ReferenceField(User, blank=True, null=True, default=None)
    # The platform that this job can run on.
    platform = models.CharField(max_length=50)
    # Job environment string.
    environment_string = models.CharField(max_length=200, blank=True, null=True, default=None)
    # Template to use, if any.
    template = models.ForeignKey(to=JobTemplate, on_delete=models.CASCADE, blank=True, null=True, default=None)
    # Blobstore path of the custom binary for this job.
    custom_binary_path = models.CharField(max_length=50, blank=True, null=True, default=None)
    # Filename for the custom binary.
    custom_binary_filename = models.CharField(max_length=50, blank=True, null=True, default=None)
    # Revision of the custom binary.
    custom_binary_revision = models.IntegerField(blank=True, null=True, default=1)