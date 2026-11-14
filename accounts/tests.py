from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AccountFeatureTests(TestCase):
    def setUp(self):
        self.staff = CustomUser.objects.create_user(
            username='staff1', password='ValidPass123!', email='staff@example.com', role='STAFF'
        )
        self.mechanic = CustomUser.objects.create_user(
            username='mechanic1', password='ValidPass123!', email='mechanic@example.com', role='MECHANIC'
        )
        self.owner = CustomUser.objects.create_user(
            username='owner1', password='ValidPass123!', email='owner@example.com', role='OWNER'
        )

    def test_registration_hashes_password_and_rejects_duplicate_username_or_email(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newstaff', 'email': 'new@example.com', 'first_name': 'New',
            'last_name': 'Staff', 'contact_number': '09123456789', 'role': 'STAFF',
            'password1': 'GoodPassword123!', 'password2': 'GoodPassword123!',
        })
        self.assertRedirects(response, reverse('login'))
        user = CustomUser.objects.get(username='newstaff')
        self.assertTrue(user.check_password('GoodPassword123!'))
        self.assertNotEqual(user.password, 'GoodPassword123!')
        for username, email in [('STAFF1', 'other@example.com'), ('other', 'STAFF@example.com')]:
            response = self.client.post(reverse('signup'), {
                'username': username, 'email': email, 'role': 'STAFF',
                'password1': 'GoodPassword123!', 'password2': 'GoodPassword123!',
            })
            self.assertEqual(response.status_code, 200)
            self.assertFalse(CustomUser.objects.filter(email=email).exists())

    def test_login_role_dashboards_and_role_restrictions(self):
        for user, role, name in [
            (self.owner, 'OWNER', 'owner_dashboard'),
            (self.staff, 'STAFF', 'staff_dashboard'),
            (self.mechanic, 'MECHANIC', 'mechanic_dashboard'),
        ]:
            self.client.logout()
            self.assertTrue(self.client.login(username=user.username, password='ValidPass123!'))
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
            for other_role, other_name in [('OWNER', 'owner_dashboard'), ('STAFF', 'staff_dashboard'), ('MECHANIC', 'mechanic_dashboard')]:
                response = self.client.get(reverse(other_name))
                if other_role == role:
                    self.assertEqual(response.status_code, 200)
                else:
                    self.assertEqual(response.status_code, 302)

    def test_profile_protected_and_contact_can_be_updated(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("profile")}')
        self.client.force_login(self.staff)
        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Updated', 'last_name': 'Staff', 'email': 'updated@example.com',
            'contact_number': '09112223333',
        })
        self.assertRedirects(response, reverse('profile'))
        self.staff.refresh_from_db()
        self.assertEqual(self.staff.contact_number, '09112223333')
        self.assertEqual(self.staff.email, 'updated@example.com')

    def test_logout_ends_session(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertRedirects(self.client.get(reverse('profile')), f'{reverse("login")}?next={reverse("profile")}')
