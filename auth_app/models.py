from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class CustomUser(AbstractUser):
    """
    CustomUser model extending the default Django User model.

    This model replaces the username with an email for authentication
    and adds additional fields for user-specific information.

    Attributes:
        TYPE_CHOICES (list): Choices for the type of user (customer or business).
        username (str): Unique username for the user.
        file (FileField): Optional file upload field for user-related files.
        location (str): Location of the user.
        tel (str): Contact telephone number of the user.
        description (str): A short description about the user.
        working_hours (str): User's working hours.
        email (str): Unique email address for the user.
        created_at (date): Date when the user was created.
        type (str): Type of user (e.g., customer or business).
        is_active (bool): Whether the user's account is active.
    """

    TYPE_CHOICES = [
        ('customer', 'Kunde'),
        ('business', 'Anbieter'),
    ]
    username = models.CharField(max_length=50, unique=True)
    file = models.FileField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True, default="")
    tel = models.CharField(max_length=50, blank=True, null=True, default="")
    description = models.CharField(max_length=500, blank=True, null=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, null=True, default="")
    email = models.EmailField(unique=True)
    created_at = models.DateField(default=now)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        null=False
    )
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        Returns a string representation of the user.

        The representation includes the username, email, and user ID.

        Returns:
            str: The user's username, email, and ID.
        """

        return f'{self.username, self.email, self.id}'


class PasswordReset(models.Model):
    """
    Model for storing password reset tokens.

    Attributes:
        email (str): The email address associated with the password reset request.
        token (str): The unique token for resetting the password.
        created_at (datetime): The timestamp when the token was created.
    """

    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the password reset instance.

        The representation includes the email and the token.

        Returns:
            str: The email and token.
        """

        return f'PasswordReset(email={self.email}, token={self.token})'
