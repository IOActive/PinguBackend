from enum import Enum
from django.db import models
import uuid

class Bot(models.Model):
    class TaskStatus(models.TextChoices):
        STARTED = 'started'
        WIP = 'in-progress'
        FINISHED = 'finished'
        ERROR = 'errored out'
        NA = 'NA'
    
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """Bot health metadata."""
    # Name of the bot.
    bot_name = models.CharField(max_length=40, unique=True)

    # Time of the last heartbeat.
    last_beat_time = models.DateTimeField()

    # Task payload containing information on current task execution.
    task_payload = models.CharField(max_length=200)

    # Expected end time for task.
    task_end_time = models.DateTimeField()

    # Tasks status
    task_status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NA,
    )


    # Platform (esp important for Android platform for OS version).
    platform = models.CharField(max_length=50)
