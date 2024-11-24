from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from review_app.models import Review
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from auth_app.models import CustomUser
from django.db.models import Avg
import random
import json
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

    This endpoint is used to populate the database with sample data for demonstration purposes.
    It creates a set of customer and business users, each with a set of associated offers, orders, and reviews.
    The data is randomly generated and includes a variety of offer types, prices, and descriptions.
    The endpoint returns a JSON response with a success message and a HTTP status code of 200.
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

        CustomUser.objects.filter(username__startswith='demo_').delete()
        Offer.objects.filter(user__username__startswith='demo_').delete()
        Review.objects.filter(reviewer__username__startswith='demo_').delete()
        Order.objects.filter(customer_user__username__startswith='demo_').delete()

        customer_names = [
            "Max Mustermann", "Erika Musterfrau", "Hans Meier", "Anna Schmidt",
            "Peter Müller", "Julia Schneider", "Thomas Weber", "Claudia Fischer",
            "Markus Bauer", "Sabrina Hoffmann"
        ]
        order_descriptions = [
            "Ein umfassender Service, der auf die Bedürfnisse des Kunden zugeschnitten ist.",
            "Effiziente und hochwertige Softwarelösungen, pünktlich geliefert.",
            "Individuelle Entwicklung mit außergewöhnlicher Liebe zum Detail.",
            "Innovative Lösungen, die die Erwartungen übertreffen.",
            "Personalisierte Dienstleistungen, die auf die Erreichung von Geschäftszielen ausgerichtet sind.",
            "Hochleistungsfähige Systeme, entwickelt mit modernster Technologie.",
            "Zuverlässige und skalierbare Lösungen für wachsende Unternehmen.",
            "Kosteneffiziente Dienstleistungen, ohne Kompromisse bei der Qualität.",
            "Umfassende Unterstützung für eine nahtlose Projektausführung.",
            "Kreative und einzigartige Lösungen für komplexe Probleme.",
            "Spitzenleistungen mit einem Fokus auf Kundenzufriedenheit."
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
        
        # Dynamisch Avatar-Dateinamen basierend auf Vornamen der Business-Nutzer erstellen
        business_descriptions = [
            "Ein führendes Unternehmen in der IT-Branche, das innovative Lösungen für komplexe Herausforderungen bietet.",
            "Bekannt für zuverlässige und skalierbare Softwarelösungen, die den Anforderungen moderner Unternehmen gerecht werden.",
            "Wir bieten maßgeschneiderte digitale Lösungen, um Ihr Geschäft auf die nächste Stufe zu bringen.",
            "Experten für kreative und effiziente IT-Dienstleistungen mit einem Fokus auf Qualität und Kundenzufriedenheit.",
            "Unsere Mission ist es, durch Spitzentechnologie und Expertise außergewöhnliche Ergebnisse zu liefern.",
            "Ihr vertrauenswürdiger Partner für umfassende IT-Dienstleistungen, die langfristige Erfolge sichern.",
            "Innovative Technologien kombiniert mit praktischen Lösungen für nachhaltige Geschäftsentwicklung.",
            "Spezialisiert auf moderne und zukunftsorientierte IT-Strategien, die Ihrem Unternehmen einen Vorsprung verschaffen.",
            "Wir entwickeln digitale Produkte, die durch Kreativität und technisches Know-how überzeugen.",
            "Ihr Experte für flexible und agile IT-Lösungen, die sich den sich ändernden Anforderungen Ihres Unternehmens anpassen."
        ]
        
        for i, name in enumerate(business_names):
            first_name, last_name = random.choice(customer_names).split(" ")
            
            # Avatar-Dateiname basierend auf dem Vornamen
            avatar_filename = f"/avatar/{first_name.lower()}_avatar.jpg"

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
                description=random.choice(business_descriptions),
                working_hours=f'{random.randint(8, 10)}:00 - {random.randint(16, 18)}:00',
                file=avatar_filename  # Avatar basierend auf dem Vornamen
            )
            business_users.append(user)
 
            offer_titles = [
                "Umfassende Softwareentwicklung",
                "Maßgeschneiderte IT-Lösungen",
                "Individuelle Webanwendungen",
                "Unternehmenssoftware-Dienstleistungen",
                "Mobile App-Entwicklung",
                "Full-Stack-Entwicklungsexpertise",
                "Innovative Softwarelösungen",
                "Agile Softwareentwicklung",
                "Individuelle digitale Lösungen",
                "Modernste Cloud-Dienste"
            ]

            offer_descriptions = [
                "Hochwertige Softwareentwicklung für Unternehmen jeder Größe.",
                "Maßgeschneiderte Lösungen, um Ihre einzigartigen geschäftlichen Herausforderungen zu meistern.",
                "Zuverlässige und skalierbare Dienstleistungen zur Entwicklung von Webanwendungen.",
                "Optimierte Prozesse für außergewöhnliche Ergebnisse, pünktlich geliefert.",
                "Expertise in der Entwicklung von mobilen Apps für Android und iOS.",
                "Fortschrittliche Full-Stack-Lösungen für komplexe Anforderungen.",
                "Innovative Strategien zur Förderung der digitalen Transformation.",
                "Agile Entwicklungsmethoden für dynamische Projektanforderungen.",
                "Individuelle Lösungen, die maximale Effizienz bieten.",
                "Sichere und optimierte Cloud-Dienste zur Steigerung der Leistung."
            ]

            offer_images = [
                f'/offers/offer_{i}.jpg' for i in range(1, 11) 
            ]
            for j in range(2):
                offer = Offer.objects.create(
                    user=user,
                    title=random.choice(offer_titles),
                    description=random.choice(offer_descriptions),
                    image=random.choice(offer_images),
                )
                
                
                # Generiere eine Liste mit Preisen, ohne Duplikate zu entfernen
                # Preise in aufsteigender Reihenfolge
                prices = sorted([round(random.uniform(50, 150), 2), round(random.uniform(150, 300), 2), round(random.uniform(300, 500), 2)])

                # Lieferzeiten in aufsteigender Reihenfolge
                delivery_times = [random.randint(3, 5), random.randint(6, 8), random.randint(9, 12)]

                # Schleife zur Erstellung der OfferDetails
                for idx, (offer_type, title_suffix) in enumerate(OfferDetail.OFFER_TYPES):
                    OfferDetail.objects.create(
                        offer=offer,
                        title=f'{offer.title} - {title_suffix}',
                        revisions=random.choice([1, 3, 5]),
                        delivery_time_in_days=delivery_times[idx],  # Lieferzeit in aufsteigender Reihenfolge
                        price=prices[idx],  # Preis in aufsteigender Reihenfolge
                        features=[f"{title_suffix} Design",
                                f"{title_suffix} Hosting",
                                f"{title_suffix} Support"],
                        offer_type=offer_type
                    )

                random_date = self.random_past_date()
                offer.created_at = random_date
                offer.updated_at = random_date
                offer.save()



                
                
                
                
                customers = CustomUser.objects.filter(type='customer')
                for k in range(2): 
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
                        created_at=self.random_past_date(),
                        updated_at=self.random_past_date(),
                    )
                random_date = self.random_past_date()
                order.created_at = random_date
                order.updated_at = random_date
                order.save()
                    
                review_descriptions = [
                    "Ich war äußerst zufrieden mit dem Service, den {business_user.first_name} bereitgestellt hat. Sehr empfehlenswert für Softwareprojekte!",
                    "Ich schätzte die ausgezeichnete Kommunikation und pünktliche Lieferung von {business_user.first_name}. Tolle Erfahrung!",
                    "Die Zusammenarbeit zwischen mir und {business_user.first_name} war nahtlos und produktiv. Erstklassiger Service!",
                    "{business_user.first_name} bot mir außergewöhnliche Unterstützung und stellte sicher, dass alle Projektanforderungen erfüllt wurden.",
                    "Ich fand die von {business_user.first_name} angebotenen Lösungen innovativ und effektiv. Ein hochprofessionelles Team!",
                    "Dank {business_user.first_name} wurde mein Projekt pünktlich mit herausragenden Ergebnissen abgeschlossen.",
                    "Die Expertise und Liebe zum Detail von {business_user.first_name} beeindruckten mich. Würde definitiv empfehlen!",
                    "Ich lobe {business_user.first_name} für die Flexibilität und Fähigkeit, sich an wechselnde Bedürfnisse anzupassen.",
                    "Der Service von {business_user.first_name} übertraf meine Erwartungen in jeder Hinsicht. Hervorragende Arbeit!",
                    "Die Zusammenarbeit mit {business_user.first_name} war eine Freude für mich, der die Hingabe und Kompetenz schätzte."
                ]


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