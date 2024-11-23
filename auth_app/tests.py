from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser, PasswordReset
from rest_framework.authtoken.models import Token

class RegisterViewTests(TestCase):
    def setUp(self):
        """
        Initialize the APIClient for the test class.

        The APIClient is a test client for making API requests. It is
        initialized here so that it can be reused in each test method.

        :return: None
        """
        self.client = APIClient()

    def test_user_registration(self):
        """
        Tests that a user can be registered with the required data.

        :return: None
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "repeated_password": "securepassword123",
            "type": "customer",
            
        }
        response = self.client.post('/api/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "testuser")
        
class LoginViewTests(TestCase):
    def setUp(self):
        """
        Initialize the APIClient and the user for the test class.

        The APIClient is a test client for making API requests. It is
        initialized here so that it can be reused in each test method.

        A user is also created here with the username and password that
        will be used in the tests.

        :return: None
        """
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
        )
        self.user.is_active = True
        self.user.save()

    def test_login_success(self):
        """
        Tests that a user can be logged in with the correct credentials.

        :return: None
        """
        data = {"username": "testuser", "password": "securepassword123"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
class PasswordResetRequestTests(TestCase):
    def setUp(self):
        """
        Initialize the APIClient and the user for the test class.

        The APIClient is a test client for making API requests. It is
        initialized here so that it can be reused in each test method.

        A user is also created here with the username and password that
        will be used in the tests.

        :return: None
        """
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            is_active=True
        )

    def test_request_password_reset_success(self):
        """
        Tests that a password reset request can be sent successfully.

        :return: None
        """
        data = {"email": "testuser@example.com"}
        response = self.client.post('/api/password-reset/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

    def test_request_password_reset_invalid_email(self):
        """
        Tests that a password reset request returns a 404 when the email is not associated with any user.

        :return: None
        """
        data = {"email": "nonexistent@example.com"}
        response = self.client.post('/api/password-reset/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PasswordResetTests(TestCase):
    def setUp(self):
        """
        Initializes the APIClient, creates a user, generates a password reset token and
        saves it in the PasswordReset model.

        :return: None
        """
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
        PasswordReset.objects.create(email=self.user.email, token=self.token)

class VerifyTokenTests(TestCase):
    def setUp(self):
        """
        Initializes the APIClient, creates a user and generates a token for the user.

        The user is created with a username, email, password and is_active set to True.
        The token is generated using the Token model and saved in the database.

        :return: None
        """
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            is_active=True
        )
        self.token, created = Token.objects.get_or_create(user=self.user)  

    def test_verify_valid_token(self):
        """
        Tests that a valid token is accepted by the verify view.

        :return: None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/authentication/', {"token": self.token.key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_invalid_token(self):
        """
        Tests that an invalid token is not accepted by the verify view.

        :return: None
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken')
        response = self.client.post('/api/authentication/', {"token": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)