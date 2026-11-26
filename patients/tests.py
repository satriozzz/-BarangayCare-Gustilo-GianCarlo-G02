
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Patient, PatientVisit


class PatientVisitTests(TestCase):

    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='password123',
            role='ADMIN'
        )

        self.worker = CustomUser.objects.create_user(
            username='worker@example.com',
            email='worker@example.com',
            password='password123',
            role='HEALTH_WORKER'
        )

        self.other_worker = CustomUser.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='password123',
            role='HEALTH_WORKER'
        )

        self.patient = Patient.objects.create(
            first_name='Juan',
            last_name='Dela Cruz',
            birth_date=date(2000, 1, 1),
            sex='MALE',
            address='Cebu City',
            created_by=self.worker
        )

        self.other_patient = Patient.objects.create(
            first_name='Maria',
            last_name='Santos',
            birth_date=date(1998, 5, 10),
            sex='FEMALE',
            address='Cebu City',
            created_by=self.other_worker
        )

        self.visit = PatientVisit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            purpose='CONSULTATION',
            notes='Initial consultation',
            created_by=self.worker
        )

        self.other_visit = PatientVisit.objects.create(
            patient=self.other_patient,
            visit_date=date.today(),
            purpose='FOLLOW_UP',
            notes='Follow-up',
            created_by=self.other_worker
        )

    # TEST 1: Create a patient visit
    def test_create_visit(self):
        self.client.force_login(self.worker)

        response = self.client.post(reverse('visit_create'), {
            'patient': self.patient.id,
            'visit_date': date.today(),
            'purpose': 'CONSULTATION',
            'notes': 'New consultation'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PatientVisit.objects.count(), 3)

    # TEST 2: Reject future visit dates
    def test_future_visit_date_is_invalid(self):
        self.client.force_login(self.worker)

        response = self.client.post(reverse('visit_create'), {
            'patient': self.patient.id,
            'visit_date': date.today() + timedelta(days=1),
            'purpose': 'CONSULTATION',
            'notes': 'Future visit'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PatientVisit.objects.count(), 2)

    # TEST 3: Reject invalid visit purposes
    def test_invalid_visit_purpose(self):
        self.client.force_login(self.worker)

        response = self.client.post(reverse('visit_create'), {
            'patient': self.patient.id,
            'visit_date': date.today(),
            'purpose': 'INVALID',
            'notes': 'Invalid purpose'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PatientVisit.objects.count(), 2)

    # TEST 4: Require login
    def test_visit_requires_login(self):
        response = self.client.get(reverse('visit_list'))

        self.assertEqual(response.status_code, 302)

    # TEST 5: Prevent access to another worker's visit
    def test_cannot_view_other_workers_visit(self):
        self.client.force_login(self.worker)

        response = self.client.get(
            reverse('visit_detail', args=[self.other_visit.id])
        )

        self.assertEqual(response.status_code, 404)

    # TEST 6: Prevent editing another worker's visit
    def test_cannot_edit_other_workers_visit(self):
        self.client.force_login(self.worker)

        response = self.client.get(
            reverse('visit_update', args=[self.other_visit.id])
        )

        self.assertEqual(response.status_code, 404)

    # TEST 7: Prevent deleting another worker's visit
    def test_cannot_delete_other_workers_visit(self):
        self.client.force_login(self.worker)

        response = self.client.post(
            reverse('visit_delete', args=[self.other_visit.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(PatientVisit.objects.count(), 2)

    # TEST 8: Allow admin to view another worker's visit
    def test_admin_can_view_all_visits(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('visit_detail', args=[self.other_visit.id])
        )

        self.assertEqual(response.status_code, 200)
