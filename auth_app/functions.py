from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser
import os


def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        if not user.is_active: 
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated.')
        else:
            messages.info(request, 'Your account is already activated.')
        return redirect(os.getenv('REDIRECT_LOGIN'))
    else:
        messages.error(request, 'The activation link is invalid!')
        return redirect(os.getenv('REDIRECT_LANDING'))
