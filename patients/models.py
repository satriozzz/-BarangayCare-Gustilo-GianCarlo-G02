from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Patient(models.Model):
    SEX_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    address = models.TextField()
    contact_number = models.CharField(max_length=15, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='registered_patients'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"