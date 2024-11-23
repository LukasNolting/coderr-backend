from datetime import datetime
from django.db import models
from auth_app.models import CustomUser


class Review(models.Model):
    """
    Represents a review created by a user for a business.

    Attributes:
        business_user (ForeignKey): The business user receiving the review.
        reviewer (ForeignKey): The user who wrote the review.
        rating (int): The rating given by the reviewer (e.g., 1-5).
        description (str): The review text provided by the reviewer.
        created_at (datetime): The timestamp when the review was created.
        updated_at (datetime): The timestamp when the review was last updated.
    """

    business_user = models.ForeignKey(
        CustomUser, related_name='business_reviews', on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        CustomUser, related_name='user_reviews', on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    class Meta:
        """
        Meta configuration for the Review model.

        Ensures that each reviewer can leave only one review for a specific business user.

        Attributes:
            unique_together (tuple): Specifies that a combination of business_user and reviewer must be unique.
        """
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        """
        Returns a string representation of the review.

        Returns:
            str: A formatted string indicating the reviewer and the business user being reviewed.
        """
        return f'Review by {self.reviewer} for {self.business_user}'
