#from django.urls import path
from . import views
from .views import RegisterView, home_view, create_user, LogoutView
from django.contrib import admin
from .views import RegisterView, home_view, create_user
from .views import RegisterView
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/v1/auth/register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', views.create_user, name='create_user'),
    path('', home_view),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    
]