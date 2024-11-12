from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    Serializes 'first_name', 'last_name', and 'id' fields.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'id']


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)