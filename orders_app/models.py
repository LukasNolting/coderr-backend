from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    Represents an order placed by a customer and fulfilled by a business user.

    Attributes:
        customer_user (ForeignKey): The user who placed the order (customer).
        business_user (ForeignKey): The user who fulfills the order (business).
        title (str): The title or description of the order.
        revisions (int): The number of revisions allowed for the order.
        delivery_time_in_days (int): The time required to deliver the order in days.
        price (Decimal): The price of the order.
        features (JSONField): A list of features included in the order.
        offer_type (str): The type of the offer (e.g., "basic", "premium").
        status (str): The current status of the order ('in_progress', 'completed', 'cancelled').
        created_at (datetime): The timestamp when the order was created.
        updated_at (datetime): The timestamp when the order was last updated.
    """

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='customer_orders', on_delete=models.CASCADE
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='business_orders', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the order.

        Returns:
            str: The title of the order.
        """
        return self.title
