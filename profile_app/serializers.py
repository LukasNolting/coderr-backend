from rest_framework import serializers
from auth_app.models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id')
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'file', 
            'location', 'tel', 'description', 'working_hours', 
            'type', 'email', 'created_at', 'user'
        ]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id')
    class Meta:
        model = CustomUser
        fields = [
            'location', 'tel', 'description', 
            'working_hours', 'type', 'email', 'user', 'file', 'first_name', 'last_name'
        ]

class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name']

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = BusinessUserSerializer(source='*')

    class Meta:
        model = CustomUser
        fields = [
            'user', 'file', 'location', 'tel', 
            'description', 'working_hours', 'type'
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name']

class CustomProfileSerializer(serializers.ModelSerializer):
    user = BusinessUserSerializer(source='*')

    class Meta:
        model = CustomUser
        fields = [
            'user', 'file', 'location', 'tel', 
            'description', 'working_hours', 'type'
        ]


