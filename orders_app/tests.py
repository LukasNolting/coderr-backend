from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order

class OrderAPITests(TestCase):
    def setUp(self):
        """
        Set up test data for orders, offers, and users.
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
            description="A test offer description"
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Plan",
            revisions=2,
            delivery_time_in_days=3,
            price=100.00,
            features=["Feature A", "Feature B"],
            offer_type="basic"
        )

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Test Order",
            revisions=2,
            delivery_time_in_days=3,
            price=100.00,
            features=["Feature A", "Feature B"],
            offer_type="basic",
            status="in_progress"
        )

    def authenticate_user(self, user):
        """
        Authenticate the test client with a specific user.
        """
        self.client.force_authenticate(user=user)

    def test_get_orders(self):
        """
        Test retrieving all orders for the authenticated user.
        """
        self.authenticate_user(self.customer_user)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_order(self):
        """
        Test retrieving a single order.
        """
        self.authenticate_user(self.customer_user)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Order")

    def test_create_order(self):
        """
        Test creating a new order with valid data.
        """
        self.authenticate_user(self.customer_user)
        data = {
            "offer_detail_id": self.offer_detail.id,
            "title": "New Order",
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_create_order_invalid_user(self):
        """
        Test that a business user cannot create an order.
        """
        self.authenticate_user(self.business_user)
        data = {
            "offer_detail_id": self.offer_detail.id,
            "title": "Invalid Order",
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_status(self):
        """
        Test updating the status of an order.
        """
        self.authenticate_user(self.business_user)
        data = {"status": "completed"}
        response = self.client.patch(f'/api/orders/{self.order.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_update_order_status_invalid(self):
        """
        Test updating an order with an invalid status.
        """
        self.authenticate_user(self.business_user)
        data = {"status": "invalid_status"}
        response = self.client.patch(f'/api/orders/{self.order.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_in_progress_order_count(self):
        """
        Test retrieving the count of in-progress orders for a business user.
        """
        self.authenticate_user(self.business_user)
        response = self.client.get(f'/api/orders/order-count/{self.business_user.id}/')  # Angepasste URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 1)

    def test_get_completed_order_count(self):
        """
        Test retrieving the count of completed orders for a business user.
        """
        self.authenticate_user(self.business_user)
        response = self.client.get(f'/api/orders/completed-order-count/{self.business_user.id}/')  # Angepasste URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 0)
