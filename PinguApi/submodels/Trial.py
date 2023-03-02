from django.db import models

class Trial(models.Model):
    # App name that this trial is applied to. E.g. "d8" or "chrome".
    app_name = models.CharField(max_length=50)

    # Chance to select this set of arguments. Zero to one.
    probability = models.FloatField(default=1.0)

    # Additional arguments to apply if selected.
    app_args = models.CharField(max_length=200, default="")
