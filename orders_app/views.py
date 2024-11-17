from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Order
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
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
                "created_at": order.created_at,
                "updated_at": order.updated_at,
            }, status=status.HTTP_200_OK)
        else:
            orders = Order.objects.filter(
                Q(customer_user=request.user) | Q(business_user=request.user)
            ).values("id", "title", "status", "created_at", "updated_at")
            return Response(list(orders), status=status.HTTP_200_OK)



    def post(self, request):
        data = request.data
        offer_detail_id = data.get("offer_detail_id")
        if not offer_detail_id:
            return Response({'error': 'offer_detail_id ist erforderlich'}, status=status.HTTP_400_BAD_REQUEST)


        order = Order.objects.create(
            customer_user=request.user,
            business_user_id=2,  
            title="Generated Title",
            revisions=3,
            delivery_time_in_days=5,
            price=100.0,
            features=["Feature 1", "Feature 2"],
            offer_type="basic",
            status="in_progress"
        )
        return Response({
            "id": order.id,
            "title": order.title,
            "status": order.status,
        }, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.customer_user != request.user and order.business_user != request.user:
            return Response({'error': 'Keine Berechtigung für diese Bestellung.'}, status=status.HTTP_403_FORBIDDEN)

        status = request.data.get("status")
        if not status:
            return Response({'error': 'Status ist erforderlich'}, status=status.HTTP_400_BAD_REQUEST)

        VALID_STATUSES = ["in_progress", "completed", "cancelled"]
        if status not in VALID_STATUSES:
            return Response({'error': f'Ungültiger Status: {status}'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status
        order.save()
        return Response({
            "id": order.id,
            "title": order.title,
            "status": order.status,
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if not request.user.is_staff:
            return Response({'error': 'Nur Admins können Bestellungen löschen.'}, status=status.HTTP_403_FORBIDDEN)
        
        order.delete()
        return Response({'message': f'Bestellung mit ID {pk} wurde gelöscht.'}, status=status.HTTP_200_OK)
    
@method_decorator(csrf_exempt, name='dispatch')
class OrderCountAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:

            order_count = Order.objects.filter(business_user_id=pk, status="in_progress").count()
            return Response({'order_count': order_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Ein Fehler ist aufgetreten: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class CompletedOrderCountAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:

            completed_order_count = Order.objects.filter(business_user_id=pk, status="completed").count()
            return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Ein Fehler ist aufgetreten: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
