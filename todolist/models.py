from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    task = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    reward_points = models.IntegerField(default=0)
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.task