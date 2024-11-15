from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    Serializes 'first_name', 'last_name', and 'id' fields.
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'id']


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