from django.db import models

class JobTemplate(models.Model):
    name = models.CharField(max_length=50)
    environment_string = models.CharField(max_length=400)