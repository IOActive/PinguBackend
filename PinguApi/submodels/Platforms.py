from django.db import models

class Supported_Platforms(models.TextChoices):
        ANDROID = 'Android'
        LINUX = 'Linux'
        MAC = 'Mac'
        WINDOWS = 'Windows'
        NA = 'NA'