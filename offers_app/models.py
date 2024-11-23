from datetime import datetime
from django.db import models
from auth_app.models import CustomUser


class Offer(models.Model):
    """
    Represents an offer created by a user.

    Attributes:
        user (ForeignKey): The user who created the offer.
        title (str): The title of the offer.
        image (ImageField): An optional image associated with the offer.
        description (str): A detailed description of the offer.
        created_at (datetime): The timestamp when the offer was created.
        updated_at (datetime): The timestamp when the offer was last updated.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        """
        Returns the string representation of the offer, which is its title.

        Returns:
            str: The title of the offer.
        """
        return self.title

    def get_min_price(self):
        """
        Calculates the minimum price among all related OfferDetails.

        Returns:
            float or None: The minimum price, or None if there are no related OfferDetails.
        """
        return self.details.aggregate(models.Min('price'))['price__min']

    def get_min_delivery_time(self):
        """
        Calculates the minimum delivery time among all related OfferDetails.

        Returns:
            int or None: The minimum delivery time in days, or None if there are no related OfferDetails.
        """
        return self.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']


class OfferDetail(models.Model):
    """
    Represents a detailed version of an offer with different pricing tiers.

    Attributes:
        offer (ForeignKey): The offer to which this detail belongs.
        title (str): The title of the offer detail.
        revisions (int): The number of allowed revisions (-1 for unlimited).
        delivery_time_in_days (int): The delivery time in days for this offer detail.
        price (Decimal): The price for this offer detail.
        features (JSONField): A JSON list of features for this offer detail.
        offer_type (str): The type of the offer (basic, standard, premium).
    """
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(help_text='-1 bedeutet unendlich viele Revisionen')
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(help_text='Liste von Features als JSON-Daten')
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    class Meta:
        """
        Metadata for the OfferDetail model.

        Ensures that each combination of offer and offer_type is unique.
        """
        unique_together = ('offer', 'offer_type')

    def __str__(self):
        """
        Returns the string representation of the offer detail, which includes
        the offer's title and the offer type.

        Returns:
            str: A string in the format "<Offer Title> - <Offer Type>".
        """
        return f"{self.offer.title} - {self.offer_type.capitalize()}"
