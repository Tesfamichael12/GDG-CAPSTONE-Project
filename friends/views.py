from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from friends.serializers import FollowSerializer, UserFollowCountSerializer
from .models import Follow

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.select_related('follower', 'following')
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return self.queryset.filter(following_id=user_id).order_by('-created_at')
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        following_user = get_object_or_404(User, pk=user_id)
        
        if request.user == following_user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=following_user,
            defaults={'follower': request.user, 'following': following_user}
        )
        
        if not created:
            return Response(
                {'detail': 'Already following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).first()

        if follow:
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({'detail': 'Follow relationship does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class UserFollowCountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserFollowCountSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.filter(id=user_id)