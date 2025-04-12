from rest_framework_simplejwt.exceptions import TokenError
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer

from .models import User  # Assuming you have a custom User model


# --- Class-based registration view using DRF generic ---
class RegisterView(APIView):
    """
    This view allows new users to register by providing a username, email, and password.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request,*args,**kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If you want to add a home view, make sure it's a separate function
    def home_view(request):
        return HttpResponse("Welcome to the Home Page!")

""" Function-based registration view using serializer """
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a user using a function-based view.
    This method allows the creation of a new user with provided credentials.
    
    """
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


""" Protected view that requires authentication """
class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello {request.user.username}!"}, status=status.HTTP_200_OK)

# --- Function-based registration view using serializer ---


""" Function-based registration with manual validation """
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


""" Login View using JWT """
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return Response({"error": "Username and Password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        if user:
            """ Generate JWT Tokens """
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login Successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {'username': user.username, 'email': user.email}
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        

# def token_refresh_view(request):
#     return HttpResponse("♻️ Token refresh logic will be here.")


""" Logout functionality using JWT """
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


""" Home view (accessible to authenticated users) """
@api_view(['GET'])  # Handles GET requests
@permission_classes([IsAuthenticated])
def home_view(request):
    """
    A simple home view API that returns a welcome message.
    This can be accessed via a GET request after logging in.
    """
    return Response({"message": "Welcome to the Home View!"}, status=status.HTTP_200_OK)