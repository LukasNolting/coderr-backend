from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser, PasswordReset
from rest_framework.authtoken.models import Token

class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "repeated_password": "securepassword123",
            "type": "customer",
            
        }
        response = self.client.post('/api/registration/', data)
        print("Response data:", response.data)  # Debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "testuser")
        
class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
        )
        self.user.is_active = True
        self.user.save()

    def test_login_success(self):
        data = {"username": "testuser", "password": "securepassword123"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
class PasswordResetRequestTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            is_active=True
        )

    def test_request_password_reset_success(self):
        data = {"email": "testuser@example.com"}
        response = self.client.post('/api/password-reset/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

    def test_request_password_reset_invalid_email(self):
        data = {"email": "nonexistent@example.com"}
        response = self.client.post('/api/password-reset/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            is_active=True
        )
        from django.contrib.auth.tokens import PasswordResetTokenGenerator
        self.token_generator = PasswordResetTokenGenerator()
        self.token = self.token_generator.make_token(self.user)
        # Token in PasswordReset speichern
        PasswordReset.objects.create(email=self.user.email, token=self.token)
        print("Generated Token:", self.token)  # Debugging
        print("Database Tokens:", PasswordReset.objects.all().values())  # Debugging

class VerifyTokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            is_active=True
        )
        # Überprüfen, ob bereits ein Token existiert
        self.token, created = Token.objects.get_or_create(user=self.user)  # Token erstellen oder vorhandenes verwenden

    def test_verify_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/authentication/', {"token": self.token.key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken')
        response = self.client.post('/api/authentication/', {"token": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)