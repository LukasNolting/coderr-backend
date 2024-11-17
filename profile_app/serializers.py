from rest_framework import serializers
from auth_app.models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'file', 
            'location', 'tel', 'description', 'working_hours', 
            'type', 'email', 'created_at'
        ]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'location', 'tel', 'description', 
            'working_hours', 'type', 'email'
        ]