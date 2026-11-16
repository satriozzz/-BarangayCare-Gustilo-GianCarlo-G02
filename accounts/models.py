from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        HEALTH_WORKER = 'HEALTH_WORKER', 'Health Worker'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.HEALTH_WORKER
    )

    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username