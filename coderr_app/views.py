from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from review_app.models import Review
from offers_app.models import Offer
from auth_app.models import CustomUser
from django.db.models import Avg
import random

class BaseInfoView(APIView):
    """
    API endpoint that provides basic platform statistics, including the number of reviews,
    average rating, number of business profiles, and number of offers.
    """
    def get(self, request, *args, **kwargs):
        
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

    def get(self, request, *args, **kwargs):
        # Clear existing demo data
        CustomUser.objects.filter(username__startswith='demo_').delete()
        Offer.objects.filter(user__username__startswith='demo_').delete()
        Review.objects.filter(reviewer__username__startswith='demo_').delete()

        # Realistic names and data for IT Freelance Portal
        customer_names = [
            "Alice Becker", "John Smith", "Emily Davis", "Michael Johnson", "Sarah Lee",
            "Daniel Brown", "Laura Wilson", "Paul Green", "Sophia White", "James Harris"
        ]
        business_names = [
            "Tech Solutions Ltd.", "Code Masters", "Web Innovators", "Dev Experts",
            "Digital Builders", "NextGen IT", "FutureWorks", "Soft Solutions", "App Crafters", "Cloud Tech"
        ]
        locations = [
            "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne",
            "Stuttgart", "Dusseldorf", "Dresden", "Leipzig", "Bremen"
        ]

        # Create 10 customers
        for i, name in enumerate(customer_names):
            CustomUser.objects.create_user(
                username=f'demo_customer_{i + 1}',
                email=f'demo_customer_{i + 1}@example.com',
                password='password',
                type='customer',
                is_active=True,
                location=random.choice(locations),
            )

        business_users = []
        # Create 10 business users
        for i, name in enumerate(business_names):
            user = CustomUser.objects.create_user(
                username=f'demo_business_{i + 1}',
                email=f'demo_business_{i + 1}@example.com',
                password='password',
                type='business',
                is_active=True,
                location=random.choice(locations),
                description=f"{name} is a leading provider of IT solutions, specializing in custom software development."
            )
            business_users.append(user)

            # Create offers for each business user
            for j in range(2):
                Offer.objects.create(
                    user=user,
                    title=f'Software Development Service {j + 1} by {name}',
                    description=f'{name} offers comprehensive software development services tailored to your needs. High quality, efficient solutions delivered in record time.',
                )

        # Create reviews by customers for the existing business users and offers
        customers = CustomUser.objects.filter(type='customer')
        for business_user in business_users:
            for customer in customers:
                Review.objects.create(
                    business_user=business_user,
                    reviewer=customer,
                    rating=random.randint(3, 5),
                    description=f'{customer.username} was extremely satisfied with the service provided by {business_user.username}. Highly recommended for software projects!'
                )

        return Response({'message': 'Demo data initialized successfully.'}, status=status.HTTP_200_OK)
