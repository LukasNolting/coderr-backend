from .models import Review
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Serializes all fields of the Review model while making certain fields read-only.

    Read-only fields:
        - `reviewer`: The user who wrote the review.
        - `business_user`: The business user being reviewed.
        - `created_at`: The timestamp when the review was created.
        - `updated_at`: The timestamp when the review was last updated.
    """

    class Meta:
        """
        Meta configuration for the ReviewSerializer.

        Attributes:
            model (Model): The model to serialize (Review).
            fields (str): Specifies that all fields of the model should be serialized.
            read_only_fields (tuple): Specifies fields that should be read-only.
        """
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer', 'business_user', 'created_at', 'updated_at')
