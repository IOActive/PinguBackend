from django.db import models
from PinguApi.submodels.Job import Job

class Statistic(models.Model):
    job_id = models.ForeignKey(to=Job, on_delete=models.CASCADE)
    iteration = models.IntegerField()
    runtime = models.IntegerField()
    execs_per_sec = models.IntegerField()
    date = models.DateField()
    last_beat_time = models.DateField()
    status = models.CharField(max_length=50)
    task_payload = models.CharField(max_length=500)