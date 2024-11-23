from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser
from offers_app.models import Offer, OfferDetail

class OfferAPITests(TestCase):
    def setUp(self):
        """
        Sets up the test client, creates test users, and initializes offers and details.
        """
        self.client = APIClient()

        self.business_user = CustomUser.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepassword123",
            type="business",
            is_active=True
        )
        self.customer_user = CustomUser.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepassword123",
            type="customer",
            is_active=True
        )

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Test Offer",
            description="A test offer description",
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Plan",
            revisions=1,
            delivery_time_in_days=3,
            price=100.00,
            features=["Feature 1", "Feature 2"],
            offer_type="basic"
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Plan",
            revisions=2,
            delivery_time_in_days=5,
            price=200.00,
            features=["Feature 1", "Feature 2", "Feature 3"],
            offer_type="standard"
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Plan",
            revisions=-1,
            delivery_time_in_days=7,
            price=300.00,
            features=["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
            offer_type="premium"
        )

    def authenticate_user(self, user):
        """
        Authenticates the test client as the given user.
        """
        self.client.force_authenticate(user=user)

    def test_get_offers(self):
        """
        Tests retrieving a list of offers.
        """
        self.authenticate_user(self.business_user)
        response = self.client.get('/api/offers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_offer_details(self):
        """
        Tests retrieving details for a single offer.
        """
        self.authenticate_user(self.business_user)
        response = self.client.get(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Offer")

    def test_create_offer(self):
        """
        Tests creating a new offer with valid data.
        """
        self.authenticate_user(self.business_user)
        data = {
            "title": "New Offer",
            "description": "New offer description",
            "details": [
                {"title": "Basic", "revisions": 1, "delivery_time_in_days": 3, "price": 100, "features": ["Feature A"], "offer_type": "basic"},
                {"title": "Standard", "revisions": 2, "delivery_time_in_days": 5, "price": 200, "features": ["Feature B"], "offer_type": "standard"},
                {"title": "Premium", "revisions": -1, "delivery_time_in_days": 7, "price": 300, "features": ["Feature C"], "offer_type": "premium"}
            ]
        }

        response = self.client.post('/api/offers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)

    def test_update_offer(self):
        """
        Tests updating an existing offer.
        """
        self.authenticate_user(self.business_user)
        data = {"title": "Updated Offer Title"}
        response = self.client.patch(f'/api/offers/{self.offer.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, "Updated Offer Title")

    def test_delete_offer(self):
        """
        Tests deleting an existing offer.
        """
        self.authenticate_user(self.business_user)
        response = self.client.delete(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)

    def test_create_offer_unauthorized(self):
        """
        Tests that customers cannot create offers.
        """
        self.authenticate_user(self.customer_user)
        data = {
            "title": "Unauthorized Offer",
            "description": "Should not be allowed",
            "details": [
                {"title": "Basic", "revisions": 1, "delivery_time_in_days": 3, "price": 100, "features": ["A"], "offer_type": "basic"},
                {"title": "Standard", "revisions": 2, "delivery_time_in_days": 5, "price": 200, "features": ["A", "B"], "offer_type": "standard"},
                {"title": "Premium", "revisions": -1, "delivery_time_in_days": 7, "price": 300, "features": ["A", "B", "C"], "offer_type": "premium"}
            ]
        }
        response = self.client.post('/api/offers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_offer_creation(self):
        """
        Tests creating an offer with invalid data.
        """
        self.authenticate_user(self.business_user)
        data = {
            "title": "Invalid Offer",
            "description": "Invalid offer description",
            "details": [
                {"title": "Basic", "revisions": -2, "delivery_time_in_days": 3, "price": 100, "features": ["A"], "offer_type": "basic"}
            ]
        }
        response = self.client.post('/api/offers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
