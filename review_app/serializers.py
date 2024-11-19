from .models import Review
from auth_app import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer', 'business_user', 'created_at', 'updated_at')