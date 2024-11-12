import os
from dotenv import load_dotenv
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator

from rest_framework.authtoken.models import Token


load_dotenv()

logger = logging.getLogger(__name__)
User = get_user_model() 

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Signal receiver to create a new Token for a User instance when one is created.
    This is the default behavior of the rest_framework.authtoken app when running 
    the `createauthtoken` management command.

    Args:
        sender (User): The User model class.
        instance (User): The User instance being saved.
        created (bool): Whether the instance is being created (True) or updated (False).
    """
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User) 
def send_activation_email(sender, instance, created, **kwargs):
    """
    Signal receiver to send an activation email to a User instance when
    one is created and not yet activated.

    Args:
        sender (User): The User model class
        instance (User): The User instance being saved
        created (bool): Whether the instance is being created (True) or updated (False)
    """
    if created and not instance.is_active:
        token = token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        activation_url = reverse('activate_user', kwargs={'uidb64': uid, 'token': token})
        full_url = f'{settings.DOMAIN_NAME}{activation_url}'
        domain_url = os.getenv('REDIRECT_LANDING')
        text_content = render_to_string(
            "emails/activation_email.txt",
            context={'user': instance, 'activation_url': full_url, 'domain_url': domain_url},
        )
        html_content = render_to_string(
            "emails/activation_email.html",
            context={'user': instance, 'activation_url': full_url, 'domain_url': domain_url},
        )
        subject = 'Confirm your email'
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()