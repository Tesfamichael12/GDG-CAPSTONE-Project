from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer


"""
ViewSet for viewing and editing user profiles.
"""
class UserProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_class = [IsAuthenticated]
    
    queryset = Profile.objects.all()

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Profile.objects.filter(user_id=user_id)
    
    def perform_create(self, serializer):
        # Create Profile for the User
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        serializer.save(user=user)
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()

        if profile.user != request.user:
            return Response({"error": "you are not authorized to update this Profile."}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)
    
"""
View for sending and accepting friend requests.
"""
class FriendRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        receiver = get_object_or_404(User, id=user_id)
        sender = request.user

        if sender == receiver:
            return Response({"error": "You cannot send a Friend Request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        sender_profile = sender.profile
        receiver_profile = receiver.profile

        # Check if there is an existing relationship request
        existing_request = Relationship.objects.filter(
            sender=sender_profile, receiver=recevier_profile
        ).first()

        if existing_request:
            if existing_request.status == 'send':
                return Response({"message": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
            elif existing_request.status == 'accepted':
                return Response({"message": "You are already Friends."}, status=status.HTTP_200_OK)


        # Create a new request
        relationship = Relationship.objects.create(
            sender=sender_profile, receiver=receiver_profile, status='send'
        )
        return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)

    def put(self, request, user_id):
        sender = request.user
        receiver = get_object_or_404(User, id=user_id)

        sender_profile = sender.profile
        receiver_profile = receiver.profile

        # Check if the relationship exists
        relationship = Relationship.objects.filter(sender=receiver_profile, receiver=sender_profile, status='send').first()

        if relationship:
            relationship.status = 'accepted'
            relationship.save()
            sender_profile.friends.add(receiver)
            receiver_profile.friends.add(sender)
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
