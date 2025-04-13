from django.urls import path, include  # 'include' is used below for including router URLs
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet, 
    LikeViewSet
)

comment_router = DefaultRouter()
comment_router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('posts/<int:post_id>/', include(comment_router.urls)),
    path('posts/<int:post_id>/like/', LikeViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:post_id>/unlike/', LikeViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
