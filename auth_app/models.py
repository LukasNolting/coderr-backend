from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    CustomUser model extending the default Django User model.
    Username is replaced by email for authentication.
    """
    CATEGORY_CHOICES = [
        ('customer', 'Kunde'),
        ('business', 'Anbieter'),
    ]
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    type = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=False,
        null=False
    )    
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        String representation of the user, showing first and last name.
        """

        return f'{self.username,self.email,self.id}'

class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)