from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .models import Offer, OfferDetail
from .serializers import OfferSerializer
from django.core.exceptions import ObjectDoesNotExist


from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Offer
from .serializers import OfferSerializer


class OfferView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                offer = Offer.objects.get(pk=pk)
                serializer = OfferSerializer(offer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Offer.DoesNotExist:
                return Response({'error': 'Angebot nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)
        else:

            offers = Offer.objects.all()


            creator_id = request.query_params.get('creator_id')
            if creator_id:
                offers = offers.filter(user_id=creator_id)


            search = request.query_params.get('search')
            if search:
                offers = offers.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )


            max_delivery_time = request.query_params.get('max_delivery_time')
            if max_delivery_time:
                offers = offers.filter(details__delivery_time_in_days__lte=max_delivery_time)


            ordering = request.query_params.get('ordering', 'updated_at')
            if ordering in ['updated_at', 'min_price']:
                offers = offers.order_by(ordering)


            paginator = PageNumberPagination()
            paginator.page_size = 10 
            result_page = paginator.paginate_queryset(offers, request)

            serializer = OfferSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            offer = Offer.objects.get(pk=pk)
            if offer.user != request.user:
                return Response({'error': 'Nicht autorisiert, dieses Angebot zu bearbeiten.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = OfferSerializer(offer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Offer.DoesNotExist:
            return Response({'error': 'Angebot nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            offer = Offer.objects.get(pk=pk)
            if offer.user != request.user:
                return Response({'error': 'Nicht autorisiert, dieses Angebot zu löschen.'}, status=status.HTTP_403_FORBIDDEN)

            offer.delete()
            return Response({'message': f'Angebot mit ID {pk} wurde gelöscht.'}, status=status.HTTP_204_NO_CONTENT)
        except Offer.DoesNotExist:
            return Response({'error': 'Angebot nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)



@method_decorator(csrf_exempt, name='dispatch')
class OfferDetailView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                detail = OfferDetail.objects.get(pk=pk)
                response_data = {
                    'id': detail.id,
                    'title': detail.title,
                    'revisions': detail.revisions,
                    'delivery_time_in_days': detail.delivery_time_in_days,
                    'price': detail.price,
                    'features': detail.features,
                    'offer_type': detail.offer_type,
                }
                return JsonResponse(response_data, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Angebotsdetail nicht gefunden'}, status=404)
        else:
            details = OfferDetail.objects.all()
            details_data = [
                {
                    'id': detail.id,
                    'title': detail.title,
                    'revisions': detail.revisions,
                    'delivery_time_in_days': detail.delivery_time_in_days,
                    'price': detail.price,
                    'features': detail.features,
                    'offer_type': detail.offer_type,
                }
                for detail in details
            ]
            return JsonResponse({'details': details_data}, status=200)
