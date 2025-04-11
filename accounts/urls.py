from django.urls import path

from .views import (
    RegisterView, create_user, LogoutView, register_view,
    login_view, home_view, MyProtectedView, register
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('api/v1/protected-route/', ProtectedView.as_view(), name='protected-route'),

    # API views
    path('register/', RegisterView.as_view(), name='register'),
    path('create-user/', create_user, name='create_user'),
    path('register-html/', register_view, name='register_html'),
    path('login-html/', login_view, name='login_html'),
    path('home/', home_view, name='home'),
    path('protected/', MyProtectedView.as_view(), name='protected'),
]
