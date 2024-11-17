from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q
from offers_app.models import Offer
from .models import Order


class OrderAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            if order.customer_user != request.user and order.business_user != request.user:
                return Response({'error': 'Keine Berechtigung für diese Bestellung.'}, status=status.HTTP_403_FORBIDDEN)

            return Response({
                "id": order.id,
                "customer_user": order.customer_user.id,
                "business_user": order.business_user.id,
                "title": order.title,
                "revisions": order.revisions,
                "delivery_time_in_days": order.delivery_time_in_days,
                "price": float(order.price),
                "features": order.features,
                "offer_type": order.offer_type,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "updated_at": order.updated_at.isoformat(),
            }, status=status.HTTP_200_OK)
        else:
            orders = Order.objects.filter(
                Q(customer_user=request.user) | Q(business_user=request.user)
            ).values("id", "title", "status", "created_at", "updated_at")
            return Response(list(orders), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if request.user.type != 'customer':
            return Response({'error': 'Nur Kunden dürfen Bestellungen erstellen.'}, status=status.HTTP_403_FORBIDDEN)

        offer_id = data.get("offer_id")
        if not offer_id:
            return Response({'error': 'Ein Angebot muss angegeben werden.'}, status=status.HTTP_400_BAD_REQUEST)

        offer = get_object_or_404(Offer, pk=offer_id)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer.user,
            title=data.get("title", offer.title),
            revisions=data.get("revisions", 0),
            delivery_time_in_days=data.get("delivery_time_in_days", 7),
            price=data.get("price", offer.get_min_price()),
            features=data.get("features", []),
            offer_type=data.get("offer_type", "basic"),
            status="in_progress",
        )

        return Response({
            "id": order.id,
            "title": order.title,
            "status": order.status,
        }, status=status.HTTP_201_CREATED)


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