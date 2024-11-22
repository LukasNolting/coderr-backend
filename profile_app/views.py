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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, pk):
        """
        Retrieves the profile of a user with the given pk.

        Args:
            request: The request object.
            pk: The primary key of the user to retrieve.

        Returns:
            A Response object with the serialized user data and a status code of 200.
        """
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        Updates the profile of a user with the given pk.

        Args:
            request: The request object.
            pk: The primary key of the user to update.

        Returns:
            A Response object with the serialized user data and a status code of 200 if the update is successful.
            A Response object with a status code of 400 if the update is not successful.
            A Response object with a status code of 403 if the request user does not have permission to update the user.

        Raises:
            PermissionDenied: If the request user does not have permission to update the user.
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
    def get(self, request):
        """
        Retrieves all business users.

        Returns:
            A Response object with the serialized business users and a status code of 200.
        """
        users = CustomUser.objects.all()
        serializer = BusinessProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Retrieves the profile of the request user.

        Returns:
            A Response object with the serialized user data and a status code of 200 if the user is found.
            A Response object with a status code of 404 if the user is not found.
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
