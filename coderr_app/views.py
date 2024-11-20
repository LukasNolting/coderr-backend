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
    Returns the count of orders for a specific business user.
    Supports general filtering or counting only completed orders.
    """

    def get(self, request, business_user_id):
        User = CustomUser
        business_user = get_object_or_404(User, pk=business_user_id)

        if 'completed-order-count' in request.resolver_match.url_name:
            order_count = Order.objects.filter(
                business_user=business_user,
                status='completed'
            ).count()
            return Response({"completed_order_count": order_count}, status=status.HTTP_200_OK)
        else:
            status_filter = request.query_params.get('status')
            orders = Order.objects.filter(business_user=business_user)

            if status_filter:
                valid_statuses = dict(Order.STATUS_CHOICES).keys()
                if status_filter not in valid_statuses:
                    return Response(
                        {"error": f"Ungültiger Status. Gültige Werte sind: {', '.join(valid_statuses)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                orders = orders.filter(status=status_filter)

            order_count = orders.count()
            return Response({"order_count": order_count}, status=status.HTTP_200_OK)

    
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
    """
    API endpoint to initialize the database with demo data.
    """
    @staticmethod
    def random_past_date(days_back=365):
        """
        Generates a random date in the past within the specified number of days.
        """
        random_days = random.randint(0, days_back)
        random_date = datetime.now() - timedelta(days=random_days)
        return random_date
    
    def get(self, request, *args, **kwargs):
        # Clear existing demo data
        CustomUser.objects.filter(username__startswith='demo_').delete()
        Offer.objects.filter(user__username__startswith='demo_').delete()
        Review.objects.filter(reviewer__username__startswith='demo_').delete()
        Order.objects.filter(customer_user__username__startswith='demo_').delete()

        # Create 10 customers with dynamic data
        customer_names = [
            "Alice Becker", "John Smith", "Emily Davis", "Michael Johnson", "Sarah Lee",
            "Daniel Brown", "Laura Wilson", "Paul Green", "Sophia White", "James Harris"
        ]
        order_descriptions = [
            "A comprehensive service tailored to the client's needs.",
            "Efficient and high-quality software solutions delivered on time.",
            "Custom development with exceptional attention to detail.",
            "Innovative solutions that exceed expectations.",
            "Personalized services designed to meet business goals.",
            "High-performance systems built with cutting-edge technology.",
            "Reliable and scalable solutions for growing businesses.",
            "Cost-effective services without compromising on quality.",
            "End-to-end support for seamless project execution.",
            "Creative and unique solutions for complex problems.",
            "Top-notch services with a focus on customer satisfaction."
        ]
        for i, name in enumerate(customer_names):
            first_name, last_name = name.split(" ")
            CustomUser.objects.create_user(
                username=f'demo_customer_{i + 1}',
                email=f'demo_customer_{i + 1}@example.com',
                password='password',
                type='customer',
                is_active=True,
                first_name=first_name,
                last_name=last_name,
                location=random.choice(['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Stuttgart', 'Dusseldorf', 'Dresden', 'Leipzig', 'Bremen']),
                tel=f'0151-{random.randint(1000000, 9999999)}',
                description=random.choice(order_descriptions),
            )

        business_users = []
        business_names = [
            "Tech Solutions Ltd.", "Code Masters", "Web Innovators", "Dev Experts",
            "Digital Builders", "NextGen IT", "FutureWorks", "Soft Solutions", "App Crafters", "Cloud Tech"
        ]
        
        avatar_images = [
            f'/avatar/user_{i}.jpg' for i in range(1, 11)  # Generiert Pfade von user_1.jpg bis user_10.jpg
        ]

        # Create 10 business users with dynamic data
        for i, name in enumerate(business_names):
            first_name, last_name = random.choice(customer_names).split(" ")
            user = CustomUser.objects.create_user(
                username=f'demo_business_{i + 1}',
                email=f'demo_business_{i + 1}@example.com',
                password='password',
                type='business',
                is_active=True,
                first_name=first_name,
                last_name=last_name,
                location=random.choice(['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Stuttgart', 'Dusseldorf', 'Dresden', 'Leipzig', 'Bremen']),
                tel=f'0151-{random.randint(1000000, 9999999)}',
                description=f'{name} is known for providing exceptional IT services and creative solutions.',
                working_hours=f'{random.randint(8, 10)}:00 - {random.randint(16, 18)}:00',
                file=random.choice(avatar_images)
            )
            business_users.append(user)
            
            offer_titles = [
                "Comprehensive Software Development",
                "Tailored IT Solutions",
                "Custom Web Applications",
                "Enterprise Software Services",
                "Mobile App Development",
                "Full-Stack Development Expertise",
                "Innovative Software Solutions",
                "Agile Software Engineering",
                "Bespoke Digital Solutions",
                "Cutting-Edge Cloud Services"
            ]
            offer_descriptions = [
                "High-quality software development for businesses of all sizes.",
                "Tailored solutions to meet your unique business challenges.",
                "Reliable and scalable web application development services.",
                "Streamlined processes to deliver exceptional results on time.",
                "Expertise in mobile app development for Android and iOS.",
                "Advanced full-stack solutions for complex requirements.",
                "Innovative strategies to enhance digital transformation.",
                "Agile development methods for dynamic project needs.",
                "Custom solutions designed for maximum efficiency.",
                "Secure and optimized cloud services to boost performance."
            ]
            offer_images = [
                f'/offers/offer_{i}.jpg' for i in range(1, 11) 
            ]
            # Create offers for each business user with dynamic data
            for j in range(2):
                offer = Offer.objects.create(
                    user=user,
                    title=random.choice(offer_titles),
                    description=random.choice(offer_descriptions),
                    image=random.choice(offer_images),
                )
                random_date = self.random_past_date()
                offer.created_at = random_date
                offer.updated_at = random_date
                offer.save()
                # Create three OfferDetails for each offer
                for offer_type, title_suffix in OfferDetail.OFFER_TYPES:
                    OfferDetail.objects.create(
                        offer=offer,
                        title=f'{offer.title} - {title_suffix}',
                        revisions=random.choice([1, 3, 5]),
                        delivery_time_in_days=random.randint(1, 10),
                        price=round(random.uniform(50, 500), 2),
                        features=[f"Key feature for {title_suffix}",
                            f"Another feature for {title_suffix}"
                        ],
                        offer_type=offer_type
                    )

                # Create orders for the current offer
                customers = CustomUser.objects.filter(type='customer')
                for k in range(2):  # Create 2 orders for each offer
                    customer = random.choice(customers)
                    offer_detail = random.choice(offer.details.all())
                    order = Order.objects.create(
                        customer_user=customer,
                        business_user=user,
                        title=f'Order for {offer_detail.title}',
                        revisions=offer_detail.revisions,
                        delivery_time_in_days=offer_detail.delivery_time_in_days,
                        price=offer_detail.price,
                        features=offer_detail.features,
                        offer_type=offer_detail.offer_type,
                        status=random.choice(['in_progress', 'completed', 'cancelled']),
                    )
                random_date = self.random_past_date()
                order.created_at = random_date
                order.updated_at = random_date
                order.save()
                    
        review_descriptions = [
                "{customer.first_name} was extremely satisfied with the service provided by {business_user.username}. Highly recommended for software projects!",
                "{customer.first_name} appreciated the excellent communication and timely delivery from {business_user.username}. Great experience!",
                "The collaboration between {customer.first_name} and {business_user.username} was seamless and productive. Top-notch service!",
                "{business_user.username} provided exceptional support to {customer.first_name}, ensuring all project requirements were met.",
                "{customer.first_name} found the solutions offered by {business_user.username} innovative and effective. A highly professional team!",
                "Thanks to {business_user.username}, {customer.first_name}'s project was completed on time with outstanding results.",
                "{business_user.username}'s expertise and attention to detail impressed {customer.first_name}. Would definitely recommend!",
                "{customer.first_name} praised {business_user.username} for their flexibility and ability to adapt to changing needs.",
                "The service from {business_user.username} exceeded {customer.first_name}'s expectations in every aspect. Excellent work!",
                "Working with {business_user.username} was a pleasure for {customer.first_name}, who appreciated their dedication and skill."
            ]
        

        # Create reviews by customers for the existing business users and offers with dynamic data
        for business_user in business_users:
            for customer in customers:
                review =Review.objects.create(
                    business_user=business_user,
                    reviewer=customer,
                    rating=random.randint(3, 5),
                    description=random.choice(review_descriptions).format(
                        customer=customer,
                        business_user=business_user
                    )
                )
                random_date = self.random_past_date()
                review.created_at = random_date
                review.updated_at = random_date
                review.save()

        return Response({'message': 'Demo data initialized successfully.'}, status=status.HTTP_200_OK)

