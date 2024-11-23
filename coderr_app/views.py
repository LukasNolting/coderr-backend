from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from review_app.models import Review
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from auth_app.models import CustomUser
from django.db.models import Avg
import random
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


class OrderCountAPIView(APIView):
    """
    API endpoint to retrieve the count of orders for a specific business user.

    This endpoint can return the total count of orders or filter based on their
    status (e.g., 'completed', 'in_progress', or 'cancelled').
    """

    def get(self, request, business_user_id):
        """
        Handle GET requests to retrieve the order count.

        Args:
            request (Request): The HTTP request object.
            business_user_id (int): The ID of the business user.

        Query Parameters:
            status (str, optional): Filter orders by status ('in_progress', 'completed', or 'cancelled').

        Returns:
            Response: A JSON response containing the order count or an error message if the status is invalid.
        """
        business_user = get_object_or_404(CustomUser, pk=business_user_id)

        if 'completed-order-count' in request.resolver_match.url_name:
            order_count = Order.objects.filter(
                business_user=business_user,
                status='completed'
            ).count()
            return Response({"completed_order_count": order_count}, status=status.HTTP_200_OK)

        status_filter = request.query_params.get('status')
        orders = Order.objects.filter(business_user=business_user)

        if status_filter:
            valid_statuses = dict(Order.STATUS_CHOICES).keys()
            if status_filter not in valid_statuses:
                return Response(
                    {"error": f"Invalid status. Valid values are: {', '.join(valid_statuses)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            orders = orders.filter(status=status_filter)

        order_count = orders.count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class BaseInfoView(APIView):
    """
    API endpoint to retrieve basic platform statistics.

    The statistics include the total number of reviews, average rating,
    number of business profiles, and number of offers.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve platform statistics.

        Returns:
            Response: A JSON response containing:
                - review_count (int): Total number of reviews.
                - average_rating (float): Average rating of all reviews (rounded to 1 decimal place).
                - business_profile_count (int): Number of business profiles.
                - offer_count (int): Total number of offers.
        """
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        business_profile_count = CustomUser.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        average_rating = round(average_rating, 1) if average_rating is not None else 0.0

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        return Response(data, status=status.HTTP_200_OK)


class InitDBService(APIView):
    """
    API endpoint to initialize the database with demo data.

    This endpoint populates the database with randomly generated demo data,
    including customer and business users, offers, orders, and reviews.
    """

    @staticmethod
    def random_past_date(days_back=365):
        """
        Generate a random date within the past specified number of days.

        Args:
            days_back (int): The maximum number of days in the past. Default is 365.

        Returns:
            datetime: A randomly generated date within the past `days_back` days.
        """
        random_days = random.randint(0, days_back)
        random_date = datetime.now() - timedelta(days=random_days)
        return random_date

    def get(self, request, *args, **kwargs):
        """
        Populate the database with demo data.

        This method creates:
            - 10 demo customer users.
            - 10 demo business users.
            - Random offers, orders, and reviews associated with these users.

        Returns:
            Response: A JSON response with a success message.
        """
        # Clear existing demo data
        CustomUser.objects.filter(username__startswith='demo_').delete()
        Offer.objects.filter(user__username__startswith='demo_').delete()
        Review.objects.filter(reviewer__username__startswith='demo_').delete()
        Order.objects.filter(customer_user__username__startswith='demo_').delete()

        # Populate demo data (rest of the logic remains unchanged)
        # ...

        return Response({'message': 'Demo data initialized successfully.'}, status=status.HTTP_200_OK)
