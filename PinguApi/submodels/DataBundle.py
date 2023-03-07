from django.db import models
import uuid

class DataBundle(models.Model):
    VALID_NAME_REGEX = models.CharField(max_length=100, blank=True, null=True, default="")
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The data bundle's name (important for identifying shared bundles).
    name = models.CharField(max_length=50)

    # Name of cloud storage bucket on GCS.
    bucket_name = models.CharField(max_length=50)

    # Data bundle's source (for accountability).
    source = models.CharField(max_length=50, blank=True, null=True, default="")

    # If data bundle can be unpacked locally or needs nfs.
    is_local = models.BooleanField(default=True)

    # Creation timestamp.
    timestamp = models.DateTimeField()

    # Whether or not bundle should be synced to worker instead.
    # Fuzzer scripts are usually run on trusted hosts, so data bundles are synced
    # there. In libFuzzer's case, we want the bundle to be on the same machine as
    # where the libFuzzer binary will run (untrusted).
    sync_to_worker = models.BooleanField(default=False)
