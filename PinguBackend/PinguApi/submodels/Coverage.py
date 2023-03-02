import datetime
from django.db import models
from PinguApi.submodels.TestCase import TestCase

class Coverage(models.Model):
    """Coverage info."""
    date = models.DateField()
    fuzzer = models.CharField(max_length=50)

    # Function coverage information.
    functions_covered = models.IntegerField()
    functions_total = models.IntegerField()

    # Edge coverage information.
    edges_covered = models.IntegerField()
    edges_total = models.IntegerField()

    # Corpus size information.
    corpus_size_units = models.IntegerField()
    corpus_size_bytes = models.IntegerField()
    corpus_location = models.CharField(max_length=200)

    # Corpus backup information.
    corpus_backup_location = models.CharField(max_length=200)

    # Quarantine size information.
    quarantine_size_units = models.IntegerField() 
    quarantine_size_bytes = models.IntegerField()
    quarantine_location = models.CharField(max_length=200)

    # Link to the HTML report.
    html_report_url = models.BinaryField()

    # References
    testcase = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
