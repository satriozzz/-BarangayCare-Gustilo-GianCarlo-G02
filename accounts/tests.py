
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AccountFeatureTests(TestCase):

    def setUp(self):
        self.staff = CustomUser.objects.create_user(
            username='staff1',
            password='ValidPass123!',
            email='staff@example.com',
            role='STAFF'
        )

        self.mechanic = CustomUser.objects.create_user(
            username='mechanic1',
            password='ValidPass123!',
            email='mechanic@example.com',
            role='MECHANIC'
        )

        self.owner = CustomUser.objects.create_user(
            username='owner1',
            password='ValidPass123!',
            email='owner@example.com',
            role='OWNER'
        )

    def test_registration_and_login_show_email_as_username(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'name="username"')

        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Username:')
        self.assertNotContains(response, 'Email address:')

    def test_registration_hashes_password_and_rejects_duplicate_username_or_email(self):
        response = self.client.post(reverse('signup'), {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'Staff',
            'contact_number': '09123456789',
            'role': 'STAFF',
            'password1': 'GoodPassword123!',
            'password2': 'GoodPassword123!',
        })

        self.assertRedirects(response, reverse('login'))

        user = CustomUser.objects.get(email='new@example.com')

        self.assertEqual(user.username, 'new@example.com')
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.check_password('GoodPassword123!'))
        self.assertNotEqual(user.password, 'GoodPassword123!')

        # Attempt to register using the same email.
        for email in ['new@example.com', 'NEW@example.com']:
            existing_count = CustomUser.objects.filter(
                email__iexact=email
            ).count()

            response = self.client.post(reverse('signup'), {
                'email': email,
                'role': 'STAFF',
                'password1': 'GoodPassword123!',
                'password2': 'GoodPassword123!',
            })

            self.assertEqual(response.status_code, 200)

            self.assertEqual(
                CustomUser.objects.filter(email__iexact=email).count(),
                existing_count
            )

        # Attempt to register using an email already owned by another account.
        existing_count = CustomUser.objects.filter(
            email__iexact='staff@example.com'
        ).count()

        response = self.client.post(reverse('signup'), {
            'email': 'STAFF@example.com',
            'role': 'STAFF',
            'password1': 'GoodPassword123!',
            'password2': 'GoodPassword123!',
        })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            CustomUser.objects.filter(
                email__iexact='staff@example.com'
            ).count(),
            existing_count
        )

    def test_login_role_dashboards_and_role_restrictions(self):
        for user, role, dashboard in [
            (self.owner, 'OWNER', 'owner_dashboard'),
            (self.staff, 'STAFF', 'staff_dashboard'),
            (self.mechanic, 'MECHANIC', 'mechanic_dashboard'),
        ]:
            self.client.logout()

            response = self.client.post(reverse('login'), {
                'username': user.email.upper(),
                'password': 'ValidPass123!',
            })

            self.assertRedirects(response, reverse(dashboard))

            for other_role, other_dashboard in [
                ('OWNER', 'owner_dashboard'),
                ('STAFF', 'staff_dashboard'),
                ('MECHANIC', 'mechanic_dashboard'),
            ]:
                response = self.client.get(reverse(other_dashboard))

                if other_role == role:
                    self.assertEqual(response.status_code, 200)
                else:
                    self.assertEqual(response.status_code, 302)

    def test_profile_protected_and_contact_can_be_updated(self):
        response = self.client.get(reverse('profile'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("profile")}'
        )

        self.client.force_login(self.staff)

        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Updated',
            'last_name': 'Staff',
            'email': 'updated@example.com',
            'contact_number': '09112223333',
        })

        self.assertRedirects(response, reverse('profile'))

        self.staff.refresh_from_db()

        self.assertEqual(self.staff.first_name, 'Updated')
        self.assertEqual(self.staff.last_name, 'Staff')
        self.assertEqual(self.staff.contact_number, '09112223333')
        self.assertEqual(self.staff.email, 'updated@example.com')
        self.assertEqual(self.staff.username, 'updated@example.com')

        self.client.logout()

        response = self.client.post(reverse('login'), {
            'username': 'UPDATED@example.com',
            'password': 'ValidPass123!',
        })

        self.assertRedirects(response, reverse('staff_dashboard'))

    def test_existing_account_can_log_in_with_case_insensitive_email(self):
        original_username = self.staff.username
        original_email = self.staff.email

        response = self.client.post(reverse('login'), {
            'username': self.staff.email.upper(),
            'password': 'ValidPass123!',
        })

        self.assertRedirects(response, reverse('staff_dashboard'))
        self.staff.refresh_from_db()
        self.assertEqual(self.staff.username, original_username)
        self.assertEqual(self.staff.email, original_email)

    def test_logout_ends_session(self):
        self.client.force_login(self.staff)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('profile'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("profile")}'
        )
