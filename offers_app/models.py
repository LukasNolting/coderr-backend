from django.db import models
from auth_app.models import CustomUser



class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_min_price(self):
        """
        Returns the minimum price of the related OfferDetails.
        """
        return self.details.aggregate(models.Min('price'))['price__min']

    def get_min_delivery_time(self):
        """
        Returns the minimum delivery time of the related OfferDetails.
        """
        return self.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']


class OfferDetail(models.Model):
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
        unique_together = ('offer', 'offer_type')  

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type.capitalize()}"
