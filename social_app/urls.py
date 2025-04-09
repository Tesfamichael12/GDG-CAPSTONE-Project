from django.contrib import admin
from django.urls import path, include
from .views import home_view, register_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    # API endpoints
    path('api/v1/', include([
        path('auth/', include([
            path('register/', register_view, name='register'),
            path('login/', TokenObtainPairView.as_view(), name='login'),
        ])),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]