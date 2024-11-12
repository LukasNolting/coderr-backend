from django.contrib import admin
from auth_app.models import CustomUser

@admin.register(CustomUser)
class CustomUserItemAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the CustomUser model.
    """
    list_display = ('email', 'username')