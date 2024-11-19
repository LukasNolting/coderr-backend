
from .models import Review
from auth_app.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListAPIView
from rest_framework import filters

class ReviewView(ListAPIView, APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['business_user']
    ordering_fields = ['updated_at']

    def get(self, request, pk=None):
        if pk:
            try:
                review = Review.objects.get(pk=pk)
                response_data = {
                    'id': review.id,
                    'business_user': review.business_user.id,
                    'reviewer': review.reviewer.id,
                    'rating': review.rating,
                    'description': review.description,
                    'created_at': review.created_at,
                    'updated_at': review.updated_at
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Review.DoesNotExist:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            reviews = self.filter_queryset(self.get_queryset())
            response_data = [
                {
                    'id': review.id,
                    'business_user': review.business_user.id,
                    'reviewer': review.reviewer.id,
                    'rating': review.rating,
                    'description': review.description,
                    'created_at': review.created_at,
                    'updated_at': review.updated_at
                }
                for review in reviews
            ]
            return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        business_user_id = request.data.get('business_user')
        reviewer = request.user
        rating = request.data.get('rating')
        description = request.data.get('description')

        if not (business_user_id and rating and description):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            business_user = CustomUser.objects.get(pk=business_user_id)
            review, created = Review.objects.get_or_create(
                business_user=business_user,
                reviewer=reviewer,
                defaults={'rating': rating, 'description': description}
            )
            if not created:
                return Response({'error': 'Review already exists for this business user'}, status=status.HTTP_400_BAD_REQUEST)
            response_data = {
                'id': review.id,
                'business_user': review.business_user.id,
                'reviewer': review.reviewer.id,
                'rating': review.rating,
                'description': review.description,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Business user not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk, reviewer=request.user)
            rating = request.data.get('rating')
            description = request.data.get('description')

            if rating:
                review.rating = rating
            if description:
                review.description = description

            review.save()
            response_data = {
                'id': review.id,
                'business_user': review.business_user.id,
                'reviewer': review.reviewer.id,
                'rating': review.rating,
                'description': review.description,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk, reviewer=request.user)
            review.delete()
            return Response({'message': f'Rezension mit ID {pk} gelöscht'}, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
