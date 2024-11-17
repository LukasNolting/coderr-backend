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
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        # Check permissions: Only the user or an admin can update the profile
        if request.user != user and not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BusinessProfileView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = BusinessProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            serializer = BusinessProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Benutzerprofil nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND,
            )
