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

class PatientVisit(models.Model):
    PURPOSE_CHOICES = [
        ('CONSULTATION', 'Consultation'),
        ('FOLLOW_UP', 'Follow-up'),
        ('VACCINATION', 'Vaccination'),
        ('MEDICINE', 'Medicine Request'),
        ('OTHER', 'Other'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits'
    )
    visit_date = models.DateField()
    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES
    )
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='recorded_visits'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        return f"{self.patient} - {self.visit_date}"