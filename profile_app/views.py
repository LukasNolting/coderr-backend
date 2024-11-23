from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from auth_app.models import CustomUser
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer, BusinessProfileSerializer, CustomProfileSerializer


class ProfileView(APIView):
    """
    API endpoint for retrieving and updating user profiles.

    Supports retrieving a specific user profile (GET) and updating
    the profile of a user (PATCH) if the request user has the necessary permissions.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        """
        Retrieve the profile of a user by primary key.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the user to retrieve.

        Returns:
            Response: A JSON response containing the serialized user data.
        """
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        Update the profile of a user by primary key.

        Args:
            request (Request): The HTTP request object containing the updated data.
            pk (int): The primary key of the user to update.

        Returns:
            Response: A JSON response containing the updated user data if successful.
            Response: A JSON response with an error message if the update fails or the user lacks permission.
        """
        user = get_object_or_404(CustomUser, pk=pk)

        if request.user != user and not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileView(APIView):
    """
    API endpoint for retrieving all business user profiles.
    """

    def get(self, request):
        """
        Retrieve all business user profiles.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized business user profiles.
        """
        users = CustomUser.objects.all()
        serializer = BusinessProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    """
    API endpoint for retrieving the profile of the authenticated user.

    Only accessible to authenticated users.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Retrieve the profile of the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the serialized user data if found.
            Response: A JSON response with an error message if the user is not found.
        """
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            serializer = BusinessProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Benutzerprofil nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND,
            )
