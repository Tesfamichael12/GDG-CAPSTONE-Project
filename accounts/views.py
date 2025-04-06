from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



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
    
    def post(self, request):
        # Handle registration logic here
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
    def home_view(request):
      return HttpResponse("Welcome to the Home Page!")
    
    
    
    def register_view(request):
     if request.method == 'POST':
        User = get_user_model()
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")

        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponse("✅ Registered successfully!")

     return render(request, '/accounts/register.html')
 
 
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully!", "user": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


# --- Function-based registration view using serializer ---
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# --- Example views for frontend testing or landing pages ---
def home_view(request):
    return HttpResponse("✅ Welcome to the homepage!")

def register_view(request):
    return HttpResponse("📄 This is the register page (HTML view)")

def login_view(request):
    return HttpResponse("🔐 This is the login page (HTML view)")

def token_refresh_view(request):
    return HttpResponse("♻️ Token refresh logic will be here.")




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