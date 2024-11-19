
from .models import Review
from auth_app.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend



from django_filters.rest_framework import DjangoFilterBackend

class ReviewView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id']  # Ermöglicht Filterung nach 'business_user'
    ordering_fields = ['updated_at']  # Ermöglicht Sortierung nach 'updated_at'

    def get(self, request, *args, **kwargs):
        # Überprüfen, ob ein Filter für 'business_user' gesetzt wurde
        business_user_id = request.query_params.get('business_user_id', None)

        if not business_user_id:
            return Response(
                {'error': 'Parameter "business_user" ist erforderlich.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtern nach dem angegebenen 'business_user'
        try:
            reviews = Review.objects.filter(business_user_id=business_user_id)
        except ValueError:
            return Response(
                {'error': 'Ungültiger Wert für "business_user".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Optional: Sortierung anwenden (falls ordering Parameter gesetzt ist)
        reviews = self.filter_queryset(reviews)

        # Serialisieren und zurückgeben
        response_data = [
            {
                'id': review.id,
                'business_user': review.business_user.id,
                'reviewer': review.reviewer.id,
                'rating': review.rating,
                'description': review.description,
                'created_at': review.created_at,
                'updated_at': review.updated_at,
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
