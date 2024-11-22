from rest_framework import serializers
from .models import Offer, OfferDetail
from decimal import Decimal

class OfferDetailSerializer(serializers.ModelSerializer):
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
        Returns the price of the offer detail as a string with two decimal places.
        If the price is not a valid number, returns "0.00".
        """
        try:
            return f"{Decimal(obj.price):.2f}"
        except (ValueError, TypeError):
            return "0.00"

class OfferSerializer(serializers.ModelSerializer):
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
        Returns the minimum price of the related OfferDetails as a string with two decimal places.
        If the minimum price is not a valid number, returns "0.00".
        """
        min_price = obj.get_min_price()
        if min_price is not None:
            return "{:.2f}".format(min_price)
        return "0.00"

    def get_min_delivery_time(self, obj):
        """
        Returns the minimum delivery time of the related OfferDetails.
        If the minimum delivery time is not a valid number, returns 0.
        """
        min_delivery_time = obj.get_min_delivery_time()
        return min_delivery_time if min_delivery_time is not None else 0

    def create(self, validated_data):      
        """
        Creates a new Offer instance with the given validated data, and
        creates three related OfferDetail instances with the data given in the
        'details' key of the validated data.

        :raises serializers.ValidationError: If the 'details' key does not contain
            exactly three dictionaries.
        :return: The newly created Offer instance.
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
        Updates an existing Offer instance with the given validated data, and
        updates or creates related OfferDetail instances with the data given in
        the 'details' key of the validated data.

        :raises serializers.ValidationError: If the 'details' key does not contain
            exactly three dictionaries.
        :param instance: The Offer instance to be updated.
        :param validated_data: A dictionary containing the data to update the
            Offer instance with.
        :return: The updated Offer instance.
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