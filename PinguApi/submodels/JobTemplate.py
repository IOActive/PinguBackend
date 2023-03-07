from django.db import models
import uuid

class JobTemplate(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    environment_string = models.CharField(max_length=400, null=True, blank=True)