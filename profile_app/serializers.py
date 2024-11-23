from rest_framework import serializers
from auth_app.models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user profiles.

    Serializes all relevant fields for a user, including their location, contact details, and profile image.

    Attributes:
        user (int): The ID of the user (mapped from the `id` field in the model).
    """
    user = serializers.IntegerField(source='id')

    class Meta:
        """
        Meta configuration for UserProfileSerializer.

        Attributes:
            model (Model): The model to serialize (CustomUser).
            fields (list): A list of fields to include in the serialization.
        """
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'file', 
            'location', 'tel', 'description', 'working_hours', 
            'type', 'email', 'created_at', 'user'
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profiles.

    Allows updating specific user profile fields, such as location, contact details, and profile image.

    Attributes:
        user (int): The ID of the user (mapped from the `id` field in the model).
    """
    user = serializers.IntegerField(source='id')

    class Meta:
        """
        Meta configuration for UserProfileUpdateSerializer.

        Attributes:
            model (Model): The model to serialize (CustomUser).
            fields (list): A list of fields to include in the serialization.
        """
        model = CustomUser
        fields = [
            'location', 'tel', 'description', 
            'working_hours', 'type', 'email', 'user', 
            'file', 'first_name', 'last_name'
        ]


class BusinessUserSerializer(serializers.ModelSerializer):
    """
    Serializer for business user information.

    Serializes the minimal fields needed to represent a business user.
    """

    class Meta:
        """
        Meta configuration for BusinessUserSerializer.

        Attributes:
            model (Model): The model to serialize (CustomUser).
            fields (list): A list of fields to include in the serialization.
        """
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name']


class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed business profiles.

    Combines business user data with additional profile information, such as location, contact details, 
    and working hours.

    Attributes:
        user (BusinessUserSerializer): A nested serializer to include basic user information.
    """
    user = BusinessUserSerializer(source='*')

    class Meta:
        """
        Meta configuration for BusinessProfileSerializer.

        Attributes:
            model (Model): The model to serialize (CustomUser).
            fields (list): A list of fields to include in the serialization.
        """
        model = CustomUser
        fields = [
            'user', 'file', 'location', 'tel', 
            'description', 'working_hours', 'type'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for custom user information.

    Serializes basic user details, such as their username, name, and primary key.
    """

    class Meta:
        """
        Meta configuration for CustomUserSerializer.

        Attributes:
            model (Model): The model to serialize (CustomUser).
            fields (list): A list of fields to include in the serialization.
        """
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name']


class CustomProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for custom profiles.

    Combines custom user data with additional profile details, such as location and working hours.

    Attributes:
        user (BusinessUserSerializer): A nested serializer to include basic user information.
    """
    user = BusinessUserSerializer(source='*')

    class Meta:
        """
        Meta configuration for CustomProfileSerializer.

        Attributes:
            model (Model): The model to serialize (CustomUser).
            fields (list): A list of fields to include in the serialization.
        """
        model = CustomUser
        fields = [
            'user', 'file', 'location', 'tel', 
            'description', 'working_hours', 'type'
        ]
