from django.urls import path, include
from rest_framework.router import DefaultRouter
from .views import UserProfileView, FriendRequestView

router = DefaultRouter()
router.register(r'profile',UserProfileView, basename="profile")

urlpatterns = [
    path('friend_request/<int:user_id>/', FriendRequestView.as_view(), name="send_friend_request"),
    path('accept_friend_request/<int:user_id>/', FriendRequestView.as_view(), name="accept_friend_request"),
    path('', include(router.urls)),
]