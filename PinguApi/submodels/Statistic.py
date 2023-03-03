from django.db import models
from PinguApi.submodels.Job import Job
import uuid

class Statistic(models.Model):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_id = models.ForeignKey(to=Job, on_delete=models.CASCADE)
    iteration = models.IntegerField()
    runtime = models.IntegerField()
    execs_per_sec = models.IntegerField()
    date = models.DateField()
    last_beat_time = models.DateField()
    status = models.CharField(max_length=50)
    task_payload = models.CharField(max_length=500)