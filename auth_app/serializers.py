from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

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
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    remember = serializers.BooleanField(required=False)

    def validate(self, data):
        """
        Validates the given data for a login request.

        :param data: A dictionary of the given data
        :return: The validated data with the user object added
        :raises: serializers.ValidationError if the credentials are invalid
        :raises: serializers.ValidationError if either email or password is empty
        """
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both fields must be filled")

        data['user'] = user
        return data        

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)