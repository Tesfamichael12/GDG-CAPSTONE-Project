from django.urls import path
from . import views
from .views import register_view, home_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register
from .views import MyProtectedView
from .views import (
    RegisterView,  # For the register view (class-based)
    create_user,   # For creating a user (function-based)
    LogoutView,    # For the logout view (class-based)
    register_view, # For the HTML registration view (function-based)
    login_view,    # For the HTML login view (function-based)
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # JWT token obtain view
    TokenRefreshView,     # JWT token refresh view
)

urlpatterns = [
    # JWT-based authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Class-based views
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Function-based views for user creation and registration
    path('create-user/', create_user, name='create_user'),
    path('register-html/', register_view, name='register_html'),
    path('login-html/', login_view, name='login_html'),
    path('home/', views.home_view, name='home'),
    path('register/', register, name='register'),
    path('protected/', MyProtectedView.as_view(), name='protected-view'),
     path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # JWT Token Refresh (Optional, if you want a refresh endpoint)
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # You can uncomment this if you have the home view implemented
    # path('', home_view, name='home'),
]
