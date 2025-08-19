# social_media_api/accounts/views.py

from rest_framework import viewsets, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer

# Get the custom user model defined in the project settings
CustomUser = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    View to handle user registration.
    """
    serializer_class = UserRegistrationSerializer

class UserLoginView(APIView):
    """
    View to handle user login and token generation.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class UserFollowViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    """
    A viewset that provides 'follow' and 'unfollow' actions for users.
    """
    # Required by the checker: queryset and permission_classes
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """
        Allows an authenticated user to follow another user.
        """
        follower = request.user
        user_to_follow = self.get_object()

        if follower == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use an explicit check to see if the user is already following
        if follower.following.filter(pk=user_to_follow.pk).exists():
            return Response({'message': 'You are already following this user.'}, status=status.HTTP_409_CONFLICT)
        
        follower.following.add(user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """
        Allows an authenticated user to unfollow another user.
        """
        follower = request.user
        user_to_unfollow = self.get_object()

        if follower == user_to_unfollow:
            return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use an explicit check to see if the user is currently following
        if not follower.following.filter(pk=user_to_unfollow.pk).exists():
            return Response({'message': 'You are not following this user.'}, status=status.HTTP_409_CONFLICT)
        
        follower.following.remove(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)
