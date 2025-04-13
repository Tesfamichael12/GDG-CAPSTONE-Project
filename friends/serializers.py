from rest_framework import serializers

from accounts.models import User
from friends.models import Follow
from users.serializers import UserSerializer

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at']
        ref_name = "FriendsFollowSerializer"  # Add a unique ref_name

    def validate(self, attrs):
        if attrs['following'] == self.context['request'].user:
            raise serializers.ValidationError("You cannot follow yourself.")
        return attrs
    
    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer()
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'created_at']

class FollowingSerializer(serializers.ModelSerializer):
    following = UserSerializer()
    
    class Meta:
        model = Follow
        fields = ['id', 'following', 'created_at']


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
