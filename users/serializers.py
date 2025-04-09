from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from .models import Profile, Relationship

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'date_joined')
        read_only_fields = ('id', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }

    def validate(self, data):
        password = data.get('password')
        if password:
            try:
                validate_password(password)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({'password': list(e.messages)})
        return data

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.
        """
        user = User.objects.create_user(**validated_data)
        # Create Profile instance for the new user
        Profile.objects.create(user=user, email=validated_data.get('email', ''))
        if 'bio' in validated_data:
            user.bio = validated_data['bio']
        user.save()  # Save the user instance to update the bio field if provided
        return user

class ProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)  # Nested UserSerializer to include user details

    class Meta:
        model = Profile
        fields = ('user', 'is_active', 'following', 'friends', 'email', 'bio', 'date_of_birth', 'profile_picture', 'date_joined')
        read_only_fields = ('user', 'date_joined')

    def get_friends_count(self, obj):
        return obj.get_friends_no()
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': UserSerializer(self.user).data
        })
        return data

