from django.http import JsonResponse
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, tokens
from .models import CustomUser
from .serializers import UserSerializer, ResetPasswordRequestSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication


class LoginView(View):
    def post(self, request):
        return JsonResponse({'message': 'Login erfolgreich'})


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

