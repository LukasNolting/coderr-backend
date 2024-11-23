from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser
from orders_app.models import Order
from review_app.models import Review
from offers_app.models import Offer, OfferDetail


class CoderrAppTests(TestCase):
    def setUp(self):
        """
        Sets up the test client, creates test users, orders, a review, an offer and an offer detail.

        The APIClient is a test client for making API requests. It is
        initialized here so that it can be reused in each test method.

        Two users are created here with the username and password that
        will be used in the tests.

        Two orders are created here with valid data. The first order has
        a status of "completed" and the second order has a status of
        "in_progress".

        A review is created here with valid data. The review is for the
        business user and the reviewer is the customer user. The rating
        is 4 and the description is "Good service!".

        An offer is created here with valid data. The offer is for the
        business user and the title is "Special Offer". The description
        is "Limited time offer!".

        An offer detail is created here with valid data. The offer detail
        is for the offer and the title is "Special Offer - Basic". The
        revisions and delivery time in days are 2 and 3 respectively. The
        price is 99.99 and the features are ["Feature 1", "Feature 2"]. The
        offer type is "basic".

        :return: None
        """
        self.client = APIClient()

        self.business_user = CustomUser.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepassword123",
            type="business",
            is_active=True,
        )

        self.customer_user = CustomUser.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepassword123",
            type="customer",
            is_active=True,
        )

        self.order_1 = Order.objects.create(
            business_user=self.business_user,
            customer_user=self.customer_user,
            status="completed",
            delivery_time_in_days=5,
            price=50.0,
        )

        self.order_2 = Order.objects.create(
            business_user=self.business_user,
            customer_user=self.customer_user,
            status="in_progress",
            delivery_time_in_days=3,
            price=30.0,
        )

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Good service!",
        )

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Special Offer",
            description="Limited time offer!",
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Special Offer - Basic",
            revisions=2,
            delivery_time_in_days=3,
            price=99.99,
            features=["Feature 1", "Feature 2"],
            offer_type="basic",
        )

    def test_order_count_api(self):
        """Test retrieving the total and completed order counts."""
        url = reverse('order-count', kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 2)

        url = reverse('completed-order-count', kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 1)

    def test_order_count_api_invalid_status(self):
        """Test order count API with invalid status."""
        url = reverse('order-count', kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url + "?status=invalid_status")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid status", response.data["error"])

    def test_base_info_view(self):
        """Test retrieving platform statistics."""
        url = reverse('base-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 1)
        self.assertEqual(response.data["average_rating"], 4.0)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)

    def test_init_db_service(self):
        """Test initializing the database with demo data."""
        url = reverse('init-db')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Demo data initialized successfully.")
