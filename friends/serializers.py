from rest_framework import serializers

from accounts.models import User
from friends.models import Follow
from users.serializers import UserSerializer

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        ref_name = "FriendsFollowSerializer"  # Add a unique ref_name


class UserFollowCountSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count', 'following_count']

    def get_followers_count(self, obj):
        return obj._followers.count()

    def get_following_count(self, obj):
        return obj._following.count()