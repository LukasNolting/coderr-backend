from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser
from review_app.models import Review


class ReviewAPITests(TestCase):
    def setUp(self):
        """
        Initializes the APIClient and creates a business user and a reviewer.
        
        A review is also created with the business user and the reviewer.
        The review_data is a dictionary containing the data for the review.
        """
        
        self.client = APIClient()

        self.business_user = CustomUser.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepassword123",
            type="business",
            is_active=True,
        )
        self.reviewer = CustomUser.objects.create_user(
            username="reviewer",
            email="reviewer@example.com",
            password="securepassword123",
            type="customer",
            is_active=True,
        )

        self.client.force_authenticate(user=self.reviewer)

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.reviewer,
            rating=5,
            description="Great service!",
        )

        self.review_data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Another great review!",
        }

    def test_get_reviews_for_business_user(self):
        """Test retrieving reviews for a specific business user."""
        url = reverse('review-list-create') + f'?business_user_id={self.business_user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 5)

    def test_get_reviews_for_current_user(self):
        """Test retrieving reviews created by the current user."""
        url = reverse('review-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], "Great service!")

    def test_create_review(self):
        """Test creating a new review for a business user."""
        new_business_user = CustomUser.objects.create_user(
            username="new_business_user",
            email="new_business@example.com",
            password="securepassword123",
            type="business",
            is_active=True,
        )

        review_data = {
            "business_user": new_business_user.id,
            "rating": 4,
            "description": "Amazing service!",
        }

        url = reverse('review-list-create')
        response = self.client.post(url, review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 4)
        self.assertEqual(response.data['description'], "Amazing service!")

    def test_create_duplicate_review(self):
        """Test that creating a duplicate review for the same business user fails."""
        url = reverse('review-list-create')
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Duplicate review",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Review already exists", response.data['error'])

    def test_update_review(self):
        """Test updating an existing review."""
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        data = {"rating": 3, "description": "Updated review"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(self.review.description, "Updated review")

    def test_update_review_unauthorized(self):
        """Test that a user cannot update a review they don't own."""
        self.client.force_authenticate(user=self.business_user)  
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        data = {"rating": 2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_review(self):
        """Test deleting a review."""
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_unauthorized(self):
        """Test that a user cannot delete a review they don't own."""
        self.client.force_authenticate(user=self.business_user)  
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
