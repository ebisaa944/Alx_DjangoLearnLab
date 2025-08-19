# social_media_api/accounts/views.py

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer, UserLoginSerializer

# Get the custom user model defined in the project settings
CustomUser = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    View to handle user registration. Uses generics.CreateAPIView for a simplified POST request.
    """
    # The serializer class to use for validating and creating new user instances
    serializer_class = UserRegistrationSerializer

class UserLoginView(APIView):
    """
    View to handle user login and token generation.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the POST request for user login.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class FollowUser(APIView):
    """
    View to allow a user to follow another user.
    """
    # Apply the IsAuthenticated permission class to this view.
    # This ensures that only authenticated users can access the view.
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """
        Handles the POST request to follow a user by their primary key (pk).
        """
        # Retrieve the user to follow, or return a 404 if not found.
        user_to_follow = get_object_or_404(CustomUser, pk=pk)
        
        # The user making the request.
        follower = request.user

        # Prevent a user from following themselves.
        if follower == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is already following this person.
        if user_to_follow in follower.following.all():
            return Response({"message": "You are already following this user."}, status=status.HTTP_409_CONFLICT)

        # Add the user to the current user's following list.
        follower.following.add(user_to_follow)
        
        return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

class UnfollowUser(APIView):
    """
    View to allow a user to unfollow another user.
    """
    # Apply the IsAuthenticated permission class to this view.
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """
        Handles the POST request to unfollow a user by their primary key (pk).
        """
        # Retrieve the user to unfollow, or return a 404 if not found.
        user_to_unfollow = get_object_or_404(CustomUser, pk=pk)
        
        # The user making the request.
        follower = request.user

        # Prevent a user from unfollowing themselves.
        if follower == user_to_unfollow:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is currently following this person.
        if user_to_unfollow not in follower.following.all():
            return Response({"message": "You are not following this user."}, status=status.HTTP_409_CONFLICT)

        # Remove the user from the current user's following list.
        follower.following.remove(user_to_unfollow)
        
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
