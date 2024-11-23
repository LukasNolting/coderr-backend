from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    Handles the creation of new users, ensuring password validation
    and providing fields for 'email', 'username', 'password',
    'repeated_password', and 'type'.
    """

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """
        Validate that passwords match and 'type' is either 'customer' or 'business'.

        Args:
            data (dict): Input data from the user.

        Returns:
            dict: Validated data.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """

        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return data

    def create(self, validated_data):
        """
        Create a new user instance after stripping out 'repeated_password'.

        Args:
            validated_data (dict): Validated data from the serializer.

        Returns:
            CustomUser: The created user instance.
        """

        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Validates login credentials, including 'username', 'password', and an optional
    'remember' field for session persistence.
    """

    username = serializers.CharField()
    password = serializers.CharField()
    remember = serializers.BooleanField(required=False)

    def validate(self, data):
        """
        Validate the provided login credentials.

        Args:
            data (dict): Input data for login.

        Returns:
            dict: Validated data including the authenticated user.

        Raises:
            serializers.ValidationError: If credentials are invalid or fields are empty.
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
    """
    Serializer for requesting a password reset.

    Validates that a valid email is provided.
    """

    email = serializers.EmailField(required=True)
