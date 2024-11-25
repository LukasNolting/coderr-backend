from rest_framework import serializers
from .models import Offer, OfferDetail
from decimal import Decimal


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferDetail model.

    Serializes the details of an offer, including its price, title, delivery time,
    and associated features.
    """
    price = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'offer',
            'offer_id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]

    def get_price(self, obj):
        """
        Get the price of the offer detail formatted as a string with two decimal places.

        Args:
            obj (OfferDetail): The OfferDetail instance.

        Returns:
            str: The formatted price as a string (e.g., "123.45").
                Returns "0.00" if the price is invalid.
        """
        try:
            return f"{Decimal(obj.price):.2f}"
        except (ValueError, TypeError):
            return "0.00"


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model.

    Serializes offers along with their details, including minimum price,
    minimum delivery time, and associated user.
    """
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user'
        ]
        read_only_fields = ['user']

    def get_min_price(self, obj):
        """
        Get the minimum price among the related OfferDetails.

        Args:
            obj (Offer): The Offer instance.

        Returns:
            str: The minimum price as a string with two decimal places (e.g., "123.45").
                Returns "0.00" if no OfferDetails are associated.
        """
        min_price = obj.get_min_price()
        if min_price is not None:
            return "{:.2f}".format(min_price)
        return "0.00"

    def get_min_delivery_time(self, obj):
        """
        Get the minimum delivery time among the related OfferDetails.

        Args:
            obj (Offer): The Offer instance.

        Returns:
            int: The minimum delivery time in days. Returns 0 if no OfferDetails are associated.
        """
        min_delivery_time = obj.get_min_delivery_time()
        return min_delivery_time if min_delivery_time is not None else 0

    def create(self, validated_data):
        """
        Create a new Offer instance and its related OfferDetails.

        Args:
            validated_data (dict): The validated data for creating the Offer.

        Raises:
            serializers.ValidationError: If the 'details' field does not contain
            exactly three OfferDetails.

        Returns:
            Offer: The created Offer instance.
        """
        details_data = validated_data.pop('details', [])
        if len(details_data) != 3:
            raise serializers.ValidationError("Es müssen genau drei Angebotsdetails angegeben werden.")

        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        """
        Update an existing Offer instance and its related OfferDetails.

        Args:
            instance (Offer): The Offer instance to update.
            validated_data (dict): The validated data for updating the Offer.

        Raises:
            serializers.ValidationError: If the 'details' field does not contain
            exactly three OfferDetails.

        Returns:
            Offer: The updated Offer instance.
        """
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)
        return instance
