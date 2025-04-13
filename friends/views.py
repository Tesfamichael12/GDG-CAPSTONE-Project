from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from accounts.models import User
from friends.serializers import FollowSerializer, FollowerSerializer, FollowingSerializer, UserFollowCountSerializer
from .models import Follow


class FollowViewSet(viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def follow(self, request, user_id=None):
        user_to_follow = get_object_or_404(User, pk=user_id)
        if user_to_follow == request.user:
            return Response({"message": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_201_CREATED)
        return Response({"message": f"You are already following {user_to_follow.username}"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def unfollow(self, request, user_id=None):
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        if follow.exists():
            follow.delete()
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        return Response({"message": f"You are not following {user_to_unfollow.username}"}, status=status.HTTP_400_BAD_REQUEST)

class FollowersListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Follow.objects.filter(following_id=user_id)

class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Follow.objects.filter(follower_id=user_id)
        

class UserFollowCountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserFollowCountSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.filter(id=user_id)
