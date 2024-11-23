from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import timedelta
from django.views import View
from django.utils import timezone, http
from django.urls import reverse
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator as token_generator
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, tokens
from .models import CustomUser, PasswordReset
from .serializers import UserSerializer, ResetPasswordRequestSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
import os
from django.template.loader import render_to_string
from dotenv import load_dotenv
from django.core.mail import EmailMultiAlternatives
from .serializers import LoginSerializer

load_dotenv()


class LoginView(APIView):
    """
    Handles user login.

    This view authenticates users and provides them with an authentication token
    upon successful login.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Args:
            request (Request): The HTTP request containing the user credentials.

        Returns:
            Response: JSON response containing:
                - 'token': Authentication token.
                - 'username': The user's username.
                - 'user_id': The user's ID.
            If authentication fails, returns a JSON response with the errors.
        """

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    """
    Handles user registration.

    Provides a view for creating new users using the CustomUser model and
    the UserSerializer serializer.
    """

    authentication_classes = []
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class RequestPasswordReset(APIView):
    """
    Handles password reset requests.

    Generates a password reset token for a user and sends an email with
    a link to reset the password.
    """

    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        """
        Handle POST requests to initiate a password reset.

        Args:
            request (Request): The request containing the user's email address.

        Returns:
            Response: A success message if the email is found, or an error
            message if the email does not correspond to a user.
        """

        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = reverse('password_reset_token', kwargs={'token': token})
            relative_reset_url = reset_url.replace('/api', '')
            domain_url = os.getenv('REDIRECT_LANDING')
            full_url = f'{domain_url}/reset-password.html?token={token}'
            prod_frontend_url = os.getenv('PROD_FRONTEND_URL')
            subject = "Coderr Passwort zurücksetzen"
            text_content = render_to_string('emails/forgot_password.txt', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
                'prod_frontend_url': prod_frontend_url,
            })
            html_content = render_to_string('emails/forgot_password.html', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
                'prod_frontend_url': prod_frontend_url,
            })
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(APIView):
    """
    Handles the password reset process.

    Allows users to validate their reset token and reset their password.
    """

    permission_classes = []

    def get(self, request, token):
        """
        Validate a password reset token.

        Args:
            request (Request): The request object.
            token (str): The token to validate.

        Returns:
            Response: A success message if the token is valid, or an error message
            if the token is invalid or expired.
        """

        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        token_lifetime = timedelta(hours=24)
        if timezone.now() > reset_obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Token is valid'}, status=status.HTTP_200_OK)

    def post(self, request, token):
        """
        Reset the user's password.

        Args:
            request (Request): The request containing the new password.
            token (str): The token used to validate the password reset request.

        Returns:
            Response: A success message if the password is updated, or an error
            message if the token is invalid or expired.
        """

        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        token_lifetime = timedelta(hours=24)
        if timezone.now() > reset_obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=reset_obj.email).first()
        if user:
            user.set_password(request.data['password'])
            user.save()
            reset_obj.delete()
            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=status.HTTP_404_NOT_FOUND)


class VerifyTokenView(APIView):
    """
    Verifies the validity of an authentication token.

    Compares the token provided by the frontend with the token in the request's
    authentication header.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Verify the token provided by the frontend.

        Args:
            request (Request): The request containing the token to verify.

        Returns:
            Response: 200 if the token is valid, or 401 if it is not.
        """

        frontend_token = request.data.get('token')
        user_token = request.auth
        
        if frontend_token == str(user_token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
