from django.contrib import admin
#from .views import ProtectedView 
from django.urls import path, include
from accounts.views import home_view, register_view, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home view
    path('', home_view, name='home'),

    # Auth API
    path('api/v1/auth/', include('accounts.urls')),  # All auth URLs (register, login, logout)
    #path('api/v1/protected-route/', ProtectedView.as_view(), name='protected-route'),
    # JWT endpoints
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
