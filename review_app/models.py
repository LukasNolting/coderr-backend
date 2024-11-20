from datetime import datetime
from django.db import models
from auth_app.models import CustomUser

class Review(models.Model):
    business_user = models.ForeignKey(CustomUser, related_name='business_reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(CustomUser, related_name='user_reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        return f'Review by {self.reviewer} for {self.business_user}'