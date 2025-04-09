from django.urls import path
from .views import FollowViewSet

urlpatterns = [
    path('follow/<int:user_id>/', FollowViewSet.as_view({'post': 'create', 'delete': 'delete'}), name="follow"),
]
