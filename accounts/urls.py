from django.urls import path
from . import views
from .views import register_view, home_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
# from .views import MyProtectedView
# from .views import (
#     RegisterView,  # For the register view (class-based)
#     create_user,   # For creating a user (function-based)
#     LogoutView,    # For the logout view (class-based)
#     register_view, # For the HTML registration view (function-based)
#     login_view,    # For the HTML login view (function-based)
# )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # JWT token obtain view
    TokenRefreshView,     # JWT token refresh view
)

urlpatterns = [
    # JWT-based authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User registration and login views
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create-user/', views.create_user, name='create_user'),
    path('home/', views.home_view, name='home'),
    path('protected/', views.MyProtectedView.as_view(), name='protected-view'),
]