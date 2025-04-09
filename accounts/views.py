from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny#, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer

from .models import User  # Assuming you have a custom User model


# --- Class-based registration view using DRF generic ---
class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        # Render an HTML form for registration
        return render(request, 'register.html')

    def post(self, request,*args,**kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If you want to add a home view, make sure it's a separate function
    def home_view(request):
        return HttpResponse("Welcome to the Home Page!")

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'User created successfully',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=201)

class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello {request.user.username}!"})

# --- Function-based registration view using serializer ---


# --- Function-based registration with manual validation ---
@api_view(['POST'])
def create_user(request):
    User = get_user_model()
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)







@api_view(['POST'])
@permission_classes([AllowAny]) 
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # or any page you want
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')

def token_refresh_view(request):
    return HttpResponse("♻️ Token refresh logic will be here.")


# --- Logout functionality using JWT ---
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token or logout failed"}, status=400)
@api_view(['GET'])  # Handles GET requests
@permission_classes([IsAuthenticated])
def home_view(request):
    """
    A simple home view API that returns a welcome message.
    This can be accessed via a GET request.
    """
    data = {"message": "Welcome to the Home View!"}
    return Response(data)
