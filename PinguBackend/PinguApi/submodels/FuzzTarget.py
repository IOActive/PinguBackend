from django.db import models
from PinguApi.submodels.Fuzzer import Fuzzer


class FuzzTarget(models.Model):
    # Selected Fuzzer
    fuzzer_engine = models.ForeignKey(to=Fuzzer, on_delete=models.CASCADE)
    # Target File
    project = models.CharField(max_length=50)
    # Binary name.
    binary = models.CharField(max_length=50)

