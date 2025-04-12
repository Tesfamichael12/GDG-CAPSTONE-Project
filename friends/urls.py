from django.urls import path
from .views import FollowViewSet, UserFollowCountViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'user-follow-counts', UserFollowCountViewSet, basename='user-follow-count')

urlpatterns = [
    path('follow/<int:user_id>/', FollowViewSet.as_view({'post': 'create', 'delete': 'delete'}), name="follow"),
    path('user-follow-count/<int:user_id>/', UserFollowCountViewSet.as_view({'get': 'retrieve'}), name="user-follow-count"),
]
