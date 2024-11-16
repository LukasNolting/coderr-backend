from rest_framework import serializers
from .models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details'
        ]
        read_only_fields = ['user'] 

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        if len(details_data) != 3:
            raise serializers.ValidationError("Es müssen genau drei Angebotsdetails angegeben werden.")
        
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)
        return instance
