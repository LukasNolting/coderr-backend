from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Q
from .models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from django.db.models import Min

class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100



class OfferAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = OfferPagination

    def get(self, request, pk=None):
        """
        Handles GET requests to retrieve a single offer or a list of offers with optional filtering, searching, and ordering.

        If a primary key (pk) is provided, it attempts to retrieve the corresponding offer
        annotated with minimum price and delivery time. If not found, returns a 404 response.

        If no pk is provided, it retrieves all offers with optional filters and search, such as:
        - Filtering by creator_id, min_price, max_price, and max_delivery_time.
        - Searching by title or description.
        - Ordering by specified fields like min_price, max_price, min_delivery_time, and updated_at.

        Applies pagination to the results and returns a paginated response of serialized offer data.
        """
        if pk:
            try:
                offer = Offer.objects.annotate(
                    min_price=Min('details__price'),
                    min_delivery_time=Min('details__delivery_time_in_days')
                ).get(pk=pk)
                serializer = OfferSerializer(offer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Offer.DoesNotExist:
                return Response({'error': 'Angebot nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)
        else:
            offers = Offer.objects.annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days')
            )

            creator_id = request.query_params.get('creator_id')
            if creator_id:
                offers = offers.filter(user_id=creator_id)

            min_price = request.query_params.get('min_price')
            if min_price:
                try:
                    min_price = float(min_price)
                    offers = offers.filter(min_price__gte=min_price)
                except ValueError:
                    return Response({'error': 'min_price muss eine gültige Zahl sein.'}, status=status.HTTP_400_BAD_REQUEST)

            max_price = request.query_params.get('max_price')
            if max_price:
                try:
                    max_price = float(max_price)
                    offers = offers.filter(details__price__lte=max_price)
                except ValueError:
                    return Response({'error': 'max_price muss eine gültige Zahl sein.'}, status=status.HTTP_400_BAD_REQUEST)

            max_delivery_time = request.query_params.get('max_delivery_time')
            if max_delivery_time:
                try:
                    max_delivery_time = int(max_delivery_time)
                    offers = offers.filter(min_delivery_time__lte=max_delivery_time)
                except ValueError:
                    return Response({'error': 'max_delivery_time muss eine ganze Zahl sein.'}, status=status.HTTP_400_BAD_REQUEST)

            search = request.query_params.get('search')
            if search:
                offers = offers.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )

            ordering = request.query_params.get('ordering')
            if ordering:
                ordering_fields = ordering.split(',')
                valid_fields = {
                    'min_price': 'min_price',
                    '-min_price': '-min_price',
                    'max_price': '-details__price',
                    'min_delivery_time': 'min_delivery_time',
                    '-min_delivery_time': '-min_delivery_time',
                    'updated_at': 'updated_at',
                    '-updated_at': '-updated_at',
                }

                resolved_ordering = [
                    valid_fields[field] for field in ordering_fields if field in valid_fields
                ]

                if resolved_ordering:
                    offers = offers.order_by(*resolved_ordering)
                else:
                    return Response(
                        {'error': f'Ungültige Sortierfelder: {ordering_fields}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                offers = offers.order_by('min_delivery_time')

            paginator = OfferPagination()
            result_page = paginator.paginate_queryset(offers, request)
            serializer = OfferSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
            
    def post(self, request):
        """
        Handles POST requests to create a new offer with its related details.

        Returns a response with the newly created offer and its details if successful.
        Otherwise, returns a 400 response with an error message.
        """
        if request.user.type != 'business':
            return Response(
                {'error': 'Nur Business-Benutzer dürfen Angebote erstellen.'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        details = data.get('details', [])
        if len(details) != 3:
            return Response(
                {'error': 'Es müssen genau drei Details angegeben werden (basic, standard, premium).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        offer_types = [detail.get('offer_type') for detail in details]
        if sorted(offer_types) != ['basic', 'premium', 'standard']:
            return Response(
                {'error': 'Die Details müssen genau die Typen basic, standard und premium enthalten.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        offer = Offer.objects.create(
            user=request.user,
            title=data.get('title'),
            description=data.get('description'),
            image=data.get('image'),
        )

        created_details = []
        for detail_data in details:
            try:
                revisions = int(detail_data.get('revisions', 0))
            except ValueError:
                return Response(
                    {'error': 'Revisions muss eine Ganzzahl sein.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if revisions < -1:
                return Response(
                    {'error': 'Revisions müssen -1 (unbegrenzt) oder größer sein.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                delivery_time_in_days = int(detail_data.get('delivery_time_in_days', 0))
            except ValueError:
                return Response(
                    {'error': 'Die Lieferzeit muss eine Ganzzahl sein.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if delivery_time_in_days <= 0:
                return Response(
                    {'error': 'Die Lieferzeit muss ein positiver Wert sein.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not detail_data.get('features', []):
                return Response(
                    {'error': 'Jedes Detail muss mindestens ein Feature enthalten.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            offer_detail = OfferDetail.objects.create(
                offer=offer,
                title=detail_data.get('title'),
                revisions=revisions,
                delivery_time_in_days=delivery_time_in_days,
                price=detail_data.get('price'),
                features=detail_data.get('features'),
                offer_type=detail_data.get('offer_type'),
            )
            created_details.append(offer_detail)

        details_serializer = OfferDetailSerializer(created_details, many=True)

        return Response({
            "id": offer.id,
            "title": offer.title,
            "description": offer.description,
            "features": offer.features,
            "details": details_serializer.data,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        """
        Handles DELETE requests to remove an existing offer.

        Validates that a primary key (pk) is provided and that the offer exists.
        Ensures that the request user is authorized to delete the offer.

        Returns:
            - 400 response if no pk is provided.
            - 404 response if the offer does not exist.
            - 403 response if the user is not authorized to delete the offer.
            - 204 response with a success message if the offer is successfully deleted.
        """
        if not pk:
            return Response(
                {'error': 'Ein Angebots-ID muss angegeben werden.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response(
                {'error': 'Angebot nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if offer.user != request.user:
            return Response(
                {'error': 'Nicht autorisiert, dieses Angebot zu löschen.'},
                status=status.HTTP_403_FORBIDDEN
            )

        offer.delete()
        return Response(
            {'message': f'Angebot mit ID {pk} wurde erfolgreich gelöscht.'},
            status=status.HTTP_204_NO_CONTENT
        )
        
    def patch(self, request, pk=None):
        """
        Handles PATCH requests to update an existing offer.

        Validates that a primary key (pk) is provided and that the offer exists.
        Ensures that the request user is authorized to update the offer.

        Returns:
            - 400 response if no pk is provided.
            - 404 response if the offer does not exist.
            - 403 response if the user is not authorized to update the offer.
            - 200 response with a success message if the offer is successfully updated.
        """
        if not pk:
            return Response(
                {'error': 'Ein Angebots-ID muss angegeben werden.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response(
                {'error': 'Angebot nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if offer.user != request.user:
            return Response(
                {'error': 'Nicht autorisiert, dieses Angebot zu bearbeiten.'},
                status=status.HTTP_403_FORBIDDEN
            )

        offer.title = request.data.get('title', offer.title)
        offer.description = request.data.get('description', offer.description)

        if 'image' in request.data:
            offer.image = request.data.get('image')

        offer.save()

        details = request.data.get('details', [])
        if details:
            for detail_data in details:
                detail_id = detail_data.get('id')

                try:
                    if detail_id:
                        detail = OfferDetail.objects.get(pk=detail_id, offer=offer)
                    else:
                        detail = OfferDetail(offer=offer)

                    detail.title = detail_data.get('title', detail.title)
                    detail.revisions = int(detail_data.get('revisions', detail.revisions))
                    detail.delivery_time_in_days = int(detail_data.get('delivery_time_in_days', detail.delivery_time_in_days))
                    detail.price = detail_data.get('price', detail.price)
                    detail.features = detail_data.get('features', detail.features)
                    detail.offer_type = detail_data.get('offer_type', detail.offer_type)

                    detail.save()

                except OfferDetail.DoesNotExist:
                    return Response(
                        {'error': f'Angebotsdetail mit ID {detail_id} nicht gefunden.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                except ValueError as e:
                    return Response(
                        {'error': f'Fehler beim Aktualisieren der Details: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
            {'message': f'Angebot mit ID {pk} wurde erfolgreich aktualisiert.'},
            status=status.HTTP_200_OK
        )


class OfferDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        GET /offers/<int:pk>/

        Returns a single offer detail with the given ID.

        GET /offers/

        Returns a list of all offer details.

        Parameters:
        pk (int): The ID of the offer detail to retrieve.

        Returns:
        Response: A JSON response containing the serialized offer detail or a list of offer details.
        """
        if pk:
            try:
                detail = OfferDetail.objects.get(pk=pk)
                serializer = OfferDetailSerializer(detail)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except OfferDetail.DoesNotExist:
                return Response({'error': 'Angebotsdetail nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)
        else:
            details = OfferDetail.objects.all()
            serializer = OfferDetailSerializer(details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
