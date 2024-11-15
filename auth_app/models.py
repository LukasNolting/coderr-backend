<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    CustomUser model extending the default Django User model.
    Username is replaced by email for authentication.
    """
    TYPE_CHOICES = [
        ('Customer', 'Customer'),
        ('Seller', 'Seller'),
    ]
    username = models.CharField(max_length=50, unique=True)
    file = models.FileField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    working_hours = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateField(blank=True, null=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
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
=======
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
    file = models.FileField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    working_hours = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    type = models.CharField(
    created_at = models.DateField(blank=True, null=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
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
>>>>>>> 864a0a107b249f5eff1c21670542051c188ca8a1
    created_at = models.DateTimeField(auto_now_add=True)