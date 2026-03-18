"""Tests for user registration, login, and profile."""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import CustomUser


class UserRegistrationTests(APITestCase):
    """Test cases for user registration."""

    def setUp(self):
        self.register_url = reverse('user-register')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test1234!',
            'password_confirm': 'Test1234!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'patient',
            'phone_number': '+1234567890',
        }

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_register_duplicate_email(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        payload = dict(self.valid_payload, password_confirm='WrongPass1!')
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_weak_password(self):
        payload = dict(self.valid_payload, password='password', password_confirm='password')
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_no_digit(self):
        payload = dict(self.valid_payload, password='NoDigitPass!', password_confirm='NoDigitPass!')
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_role(self):
        payload = dict(self.valid_payload, role='superadmin')
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(APITestCase):
    """Test cases for user login."""

    def setUp(self):
        self.login_url = reverse('user-login')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test1234!',
            first_name='Test',
            last_name='User',
            role='patient',
        )

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'Test1234!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'WrongPass!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_email(self):
        response = self.client.post(self.login_url, {
            'email': 'nobody@example.com',
            'password': 'Test1234!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields(self):
        response = self.client.post(self.login_url, {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTests(APITestCase):
    """Test cases for user profile retrieval and update."""

    def setUp(self):
        self.profile_url = reverse('user-profile')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test1234!',
            first_name='Test',
            last_name='User',
            role='patient',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['role'], 'patient')

    def test_update_profile(self):
        response = self.client.patch(self.profile_url, {
            'first_name': 'Updated',
            'phone_number': '+9876543210',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['phone_number'], '+9876543210')

    def test_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordTests(APITestCase):
    """Test cases for changing password."""

    def setUp(self):
        self.url = reverse('user-change-password')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123!',
            first_name='Test',
            last_name='User',
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        response = self.client.post(self.url, {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))

    def test_change_password_wrong_old(self):
        response = self.client.post(self.url, {
            'old_password': 'WrongOld!',
            'new_password': 'NewPass456!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
