from django.db import models

class Supported_Platforms(models.TextChoices):
        ANDROID = 'android'
        LINUX = 'linux'
        MAC = 'mac'
        WINDOWS = 'windows'
        NA = 'NA'