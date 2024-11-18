from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    business_user = models.ForeignKey(User, related_name='business_reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        return f'Review by {self.reviewer} for {self.business_user}'