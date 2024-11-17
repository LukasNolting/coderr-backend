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
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Handles login requests.

        Args:
            request (Request): The HTTP request containing the user credentials.

        Returns:
            Response: A JSON response containing the authentication token if the credentials are valid, otherwise a JSON response with the errors.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          user = serializer.validated_data['user']
          token, created = Token.objects.get_or_create(user=user)
          print('token',token)
          return Response({'token': token.key, 'username': user.username, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]
    TokenAuthentication = [AllowAny]
    CustomUser = get_user_model()
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        """
        Handles the password reset request by generating a token and sending a reset email.

        Args:
            request: The request object containing the user's email.

        The function checks if a user with the provided email exists. If the user exists,
        it generates a password reset token, saves it, and sends an email to the user
        with a reset link. If the email is not found, a 404 response is returned.

        Returns:
            Response: A success message with a 200 status if the email is sent successfully.
            Response: An error message with a 404 status if the user is not found.
        """
        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = reverse('password_reset_token', kwargs={'token': token})
            print("reset_url", reset_url)
            relative_reset_url = reset_url.replace('/api', '')
            print("relative_reset_url", relative_reset_url)
            domain_url = os.getenv('BACKEND_URL')
            print("domain_url", domain_url)
            full_url = f'http://{domain_url}/api{relative_reset_url}'
            print("full_url", full_url)
            subject = "Coderr Passwort zurücksetzen"
            text_content = render_to_string('emails/forgot_password.txt', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
            })
            html_content = render_to_string('emails/forgot_password.html', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
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
    permission_classes = []

    def get(self, request, token):
        """
        Check if the given token is valid and not expired.

        Args:
            request (Request): The request object.
            token (str): The token to check.

        Returns:
            Response: 200 with {'success': 'Token is valid'} if the token is valid and not expired.
            Response: 400 with {'error': 'Invalid token'} if the token is not valid.
            Response: 400 with {'error': 'Token expired'} if the token is expired.
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
        Resets the password for the given user

        Args:
            request: The request object
            token: The token from the password reset email

        Returns:
            A response object with a status code and a message
        """
        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=400)

        token_lifetime = timedelta(hours=24)
        if timezone.now() > reset_obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=400)

        user = CustomUser.objects.filter(email=reset_obj.email).first()
        if user:
            user.set_password(request.data['password'])
            user.save()
            reset_obj.delete()
            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)

class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Verify a token sent by the frontend is valid.

        The frontend token is compared with the user's token in the request's
        authentication header. If the two match, a 200 response is returned,
        indicating that the token is valid. If the two do not match, a 401
        response is returned, indicating that the token is not valid.

        :param request: The request object
        :return: A response with a status of 200 if the token is valid, 401 otherwise
        """
        frontend_token = request.data.get('token')
        user_token = request.auth
        
        if frontend_token == str(user_token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Handles login requests.

        Args:
            request (Request): The HTTP request containing the user credentials.

        Returns:
            Response: A JSON response containing the authentication token if the credentials are valid, otherwise a JSON response with the errors.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          user = serializer.validated_data['user']
          token, created = Token.objects.get_or_create(user=user)
          print('token',token)
          return Response({'token': token.key, 'username': user.username, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]
    TokenAuthentication = [AllowAny]
    CustomUser = get_user_model()
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        """
        Handles the password reset request by generating a token and sending a reset email.

        Args:
            request: The request object containing the user's email.

        The function checks if a user with the provided email exists. If the user exists,
        it generates a password reset token, saves it, and sends an email to the user
        with a reset link. If the email is not found, a 404 response is returned.

        Returns:
            Response: A success message with a 200 status if the email is sent successfully.
            Response: An error message with a 404 status if the user is not found.
        """
        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = reverse('password_reset_token', kwargs={'token': token})
            relative_reset_url = reset_url.replace('/coderr', '')
            custom_port_url = os.getenv('REDIRECT_LANDING') + relative_reset_url
            full_url = custom_port_url
            domain_url = os.getenv('REDIRECT_LANDING')
            subject = "Reset your password"
            text_content = render_to_string('emails/forgot_password.txt', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
            })
            html_content = render_to_string('emails/forgot_password.html', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
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
    permission_classes = []

    def get(self, request, token):
        """
        Check if the given token is valid and not expired.

        Args:
            request (Request): The request object.
            token (str): The token to check.

        Returns:
            Response: 200 with {'success': 'Token is valid'} if the token is valid and not expired.
            Response: 400 with {'error': 'Invalid token'} if the token is not valid.
            Response: 400 with {'error': 'Token expired'} if the token is expired.
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
        Resets the password for the given user

        Args:
            request: The request object
            token: The token from the password reset email

        Returns:
            A response object with a status code and a message
        """
        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=400)

        token_lifetime = timedelta(hours=24)
        if timezone.now() > reset_obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=400)

        user = CustomUser.objects.filter(email=reset_obj.email).first()
        if user:
            user.set_password(request.data['password'])
            user.save()
            reset_obj.delete()
            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)

class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Verify a token sent by the frontend is valid.

        The frontend token is compared with the user's token in the request's
        authentication header. If the two match, a 200 response is returned,
        indicating that the token is valid. If the two do not match, a 401
        response is returned, indicating that the token is not valid.

        :param request: The request object
        :return: A response with a status of 200 if the token is valid, 401 otherwise
        """
        frontend_token = request.data.get('token')
        user_token = request.auth
        
        if frontend_token == str(user_token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)