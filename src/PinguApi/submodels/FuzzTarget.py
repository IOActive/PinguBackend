from django.db import models
from PinguApi.submodels.Fuzzer import Fuzzer
import uuid


class FuzzTarget(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Selected Fuzzer
    fuzzer_engine = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE)
    # Target File
    project = models.CharField(max_length=50)
    # Binary name.
    binary = models.CharField(max_length=50)

