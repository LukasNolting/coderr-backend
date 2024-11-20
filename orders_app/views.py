from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q
from .serializers import OrderSerializer
from offers_app.models import Offer, OfferDetail
from .models import Order


class OrderAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            if order.customer_user != request.user and order.business_user != request.user:
                return Response({'error': 'Keine Berechtigung für diese Bestellung.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            orders = Order.objects.filter(
                Q(customer_user=request.user) | Q(business_user=request.user)
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if request.user.type != 'customer':
            return Response({'error': 'Nur Kunden dürfen Bestellungen erstellen.'}, status=status.HTTP_403_FORBIDDEN)

        offer_id = data.get("offer_id")
        offer_detail_id = data.get("offer_detail_id")

        if not offer_id and not offer_detail_id:
            return Response({'error': 'Ein Angebot oder OfferDetail muss angegeben werden.'}, status=status.HTTP_400_BAD_REQUEST)

        if offer_detail_id:
            offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)
            offer_id = offer_detail.offer.id  # Zuordnung zur Offer-Instanz
            revisions = offer_detail.revisions
            delivery_time_in_days = offer_detail.delivery_time_in_days
            price = offer_detail.price
            features = offer_detail.features
            offer_type = offer_detail.offer_type

        offer = get_object_or_404(Offer, pk=offer_id)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer.user,
            title=data.get("title", offer.title),
            revisions=data.get("revisions", revisions),
            delivery_time_in_days=data.get("delivery_time_in_days", delivery_time_in_days),
            price=data.get("price", price),
            features=data.get("features", features),
            offer_type=data.get("offer_type", offer_type),
            status="in_progress",
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if order.customer_user != request.user and order.business_user != request.user:
            return Response({'error': 'Keine Berechtigung für diese Bestellung.'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get("status")
        if not new_status or new_status not in dict(Order.STATUS_CHOICES).keys():
            return Response(
                {'error': 'Ungültiger oder fehlender Status. Gültige Werte sind: ' + ', '.join(dict(Order.STATUS_CHOICES).keys())},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCountAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:

            order_count = Order.objects.filter(business_user_id=pk, status="in_progress").count()
            return Response({'order_count': order_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Ein Fehler ist aufgetreten: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompletedOrderCountAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:

            completed_order_count = Order.objects.filter(business_user_id=pk, status="completed").count()
            return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Ein Fehler ist aufgetreten: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)