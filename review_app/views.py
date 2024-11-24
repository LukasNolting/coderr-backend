from .models import Review
from auth_app.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class ReviewView(ListAPIView):
    """
    API endpoint for managing reviews.

    Provides methods to:
    - Retrieve a list of reviews (filtered and ordered as specified).
    - Create a new review for a business user.
    - Partially update an existing review.
    - Delete a review.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id']
    ordering_fields = ['updated_at', 'rating']

    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of reviews based on the current user or a specific business user.

        Args:
            request (Request): The HTTP request object.

        Query Parameters:
            business_user_id (int, optional): The ID of the business user to filter reviews by.

        Returns:
            Response: A JSON response containing a list of reviews.
                    If `business_user_id` is invalid, a 400 BAD REQUEST response is returned.
        """
        current_user = request.query_params.get('reviewer_id', None)
        business_user_id = request.query_params.get('business_user_id', None)

        if business_user_id:
            try:
                reviews = Review.objects.filter(business_user_id=business_user_id)
            except ValueError:
                return Response(
                    {'error': 'Ungültiger Wert für "business_user_id".'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            reviews = Review.objects.filter(reviewer=current_user)

        reviews = self.filter_queryset(reviews)

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
        """
        Create a new review for the given business user.

        Args:
            request (Request): The HTTP request object containing review data.

        Request Body:
            business_user (int): The ID of the business user being reviewed.
            rating (int): The rating given (1-5).
            description (str): The review description.

        Returns:
            Response: A JSON response with the created review data and status 201 CREATED.
                    If a required field is missing or a review already exists, returns 400 BAD REQUEST.
                    If the business user does not exist, returns 404 NOT FOUND.
        """
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
        """
        Partially update an existing review.

        Args:
            request (Request): The HTTP request object containing the fields to update.
            pk (int): The primary key of the review to update.

        Request Body:
            rating (int, optional): The updated rating.
            description (str, optional): The updated description.

        Returns:
            Response: A JSON response with the updated review data and status 200 OK.
                    If the review does not exist or the user is not authorized, returns 404 NOT FOUND.
        """
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
        """
        Delete an existing review.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the review to delete.

        Returns:
            Response: A JSON response with a success message and status 204 NO CONTENT.
                    If the review does not exist or the user is not authorized, returns 404 NOT FOUND.
        """
        try:
            review = Review.objects.get(pk=pk, reviewer=request.user)
            review.delete()
            return Response({'message': f'Rezension mit ID {pk} gelöscht'}, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
