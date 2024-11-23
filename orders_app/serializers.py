from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Serializes all fields of the Order model and ensures that certain fields
    are read-only (e.g., `id`, `created_at`, `updated_at`).
    """

    class Meta:
        """
        Meta configuration for the OrderSerializer.

        Attributes:
            model (Model): The model class to serialize (Order).
            fields (str): Specifies that all fields of the model should be serialized.
            read_only_fields (tuple): Specifies fields that should be read-only.
        """
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the status of an order.

    Restricts serialization to the `status` field of the Order model,
    allowing partial updates for the order status.
    """

    class Meta:
        """
        Meta configuration for the OrderStatusUpdateSerializer.

        Attributes:
            model (Model): The model class to serialize (Order).
            fields (tuple): Specifies that only the `status` field should be serialized.
        """
        model = Order
        fields = ('status',)
