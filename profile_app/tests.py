from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import CustomUser

class ProfileAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.customer_user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            type="customer",
            is_active=True,
        )

        self.business_user = CustomUser.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepassword123",
            type="business",
            is_active=True,
        )

        self.staff_user = CustomUser.objects.create_user(
            username="staff_user",
            email="staff@example.com",
            password="securepassword123",
            is_staff=True,
            is_active=True,
        )

    def authenticate_user(self, user):
        """Helper method to authenticate a user."""
        self.client.force_authenticate(user=user)

    def test_get_user_profile(self):
        """Test retrieving the profile of a specific user."""
        self.authenticate_user(self.customer_user)
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)
        print(response.status_code, response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], "testuser")

    def test_get_user_profile_as_staff(self):
        """Test retrieving a user profile as a staff user."""
        self.authenticate_user(self.staff_user)
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)
        print(response.status_code, response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")

    def test_get_user_profile_unauthorized(self):
        """Test unauthorized access to another user's profile."""
        self.authenticate_user(self.business_user)
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)
        print(response.status_code)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_profile(self):
        """Test updating the profile of the authenticated user."""
        self.authenticate_user(self.customer_user)
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        data = {"location": "New Location"}
        response = self.client.patch(url, data, format='json')
        print(response.status_code, response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.location, "New Location")

    def test_update_user_profile_as_staff(self):
        """Test updating another user's profile as a staff user."""
        self.authenticate_user(self.staff_user)
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        data = {"location": "Staff Updated Location"}
        response = self.client.patch(url, data, format='json')
        print(response.status_code, response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.location, "Staff Updated Location")

    def test_get_all_business_profiles(self):
        """Test retrieving all business profiles."""
        url = reverse('business-profile')
        response = self.client.get(url)
        print(response.status_code, response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        usernames = [profile['username'] for profile in response.data]
        self.assertIn("business_user", usernames)

    def test_get_authenticated_user_profile(self):
        """Test retrieving the authenticated user's profile."""
        self.authenticate_user(self.customer_user)
        url = reverse('customer-profile')
        response = self.client.get(url)
        print(response.status_code, response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")
