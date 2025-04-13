from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment, Like
from posts.models import Post
from django.contrib.auth import get_user_model
from .serializers import (
    CommentSerializer, 
    LikeSerializer
)
from posts.permissions import IsOwnerOrReadOnly

User = get_user_model()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))
    
    def create(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LikeViewSet(viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def like(self, request, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Post already liked"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def unlike(self, request, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Post not liked yet"}, status=status.HTTP_400_BAD_REQUEST)

