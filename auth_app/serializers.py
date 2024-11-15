from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model, including handling for 'type'.
    """
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """
        Validate that passwords match and type is either 'Customer' or 'business'.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if data['type'] not in ['customer', 'business']:
            raise serializers.ValidationError("Type must be 'Customer' or 'business'.")
        
        return data

    def create(self, validated_data):
        """
        Create a new user instance after stripping out repeated_password.
        """
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)