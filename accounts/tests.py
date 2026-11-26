
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AccountFeatureTests(TestCase):

    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='ValidPass123!',
            role=CustomUser.Role.ADMIN
        )

        self.health_worker = CustomUser.objects.create_user(
            username='worker@example.com',
            email='worker@example.com',
            password='ValidPass123!',
            role=CustomUser.Role.HEALTH_WORKER
        )

    def test_login_page_uses_email_as_username(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username:')
        self.assertNotContains(response, 'name="username" type="text"')

    def test_admin_can_create_health_worker_account(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('staff_create'), {
            'email': 'newworker@example.com',
            'first_name': 'New',
            'last_name': 'Worker',
            'contact_number': '09123456789',
            'role': CustomUser.Role.HEALTH_WORKER,
            'password1': 'GoodPassword123!',
            'password2': 'GoodPassword123!',
        })

        self.assertRedirects(response, reverse('admin_dashboard'))

        user = CustomUser.objects.get(email='newworker@example.com')

        self.assertEqual(user.username, 'newworker@example.com')
        self.assertEqual(user.role, CustomUser.Role.HEALTH_WORKER)
        self.assertTrue(user.check_password('GoodPassword123!'))
        self.assertNotEqual(user.password, 'GoodPassword123!')

    def test_health_worker_cannot_create_accounts(self):
        self.client.force_login(self.health_worker)

        response = self.client.get(reverse('staff_create'))

        self.assertEqual(response.status_code, 403)

    def test_account_creation_requires_login(self):
        response = self.client.get(reverse('staff_create'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("staff_create")}'
        )

    def test_health_worker_cannot_access_admin_dashboard(self):
        self.client.force_login(self.health_worker)

        response = self.client.get(reverse('admin_dashboard'))

        self.assertRedirects(
            response,
            reverse('health_worker_dashboard')
        )

    def test_admin_cannot_access_health_worker_dashboard(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('health_worker_dashboard'))

        self.assertRedirects(
            response,
            reverse('admin_dashboard')
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("profile")}'
        )

    def test_user_can_update_own_profile(self):
        self.client.force_login(self.health_worker)

        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Updated',
            'last_name': 'Worker',
            'email': 'updated@example.com',
            'contact_number': '09112223333',
        })

        self.assertRedirects(response, reverse('profile'))

        self.health_worker.refresh_from_db()

        self.assertEqual(self.health_worker.first_name, 'Updated')
        self.assertEqual(self.health_worker.last_name, 'Worker')
        self.assertEqual(self.health_worker.email, 'updated@example.com')
        self.assertEqual(self.health_worker.username, 'updated@example.com')
        self.assertEqual(self.health_worker.contact_number, '09112223333')

    def test_user_can_log_in_with_email(self):
        response = self.client.post(reverse('login'), {
            'username': 'worker@example.com',
            'password': 'ValidPass123!',
        })

        self.assertRedirects(
            response,
            reverse('health_worker_dashboard')
        )

    def test_logout_ends_session(self):
        self.client.force_login(self.health_worker)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('profile'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("profile")}'
        )
