from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import RegisterSerializer
from django.shortcuts import render

# --- Home View (For Testing or Simple API Response) ---
@api_view(['GET'])  # Changed to GET, as this seems like a general "Home" response
def home_view(request):
    """
    A simple home view API that returns a welcome message.
    This can be accessed via a GET request.
    """
    data = {"message": "Welcome to the Home View!"}
    return Response(data)

# --- Register View (User Registration) ---
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)