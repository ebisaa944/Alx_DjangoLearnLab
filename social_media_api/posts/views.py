"""
This module defines the views for the posts app, including CRUD operations for
posts and comments, as well as a user-specific feed.
"""
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()`, and `list()` actions for posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically sets the author of a new post to the current user.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Allows a user to like a specific post.
        Uses get_object_or_404 to ensure the post exists.
        Uses get_or_create to prevent duplicate likes and handle creation.
        """
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Use get_or_create to either retrieve an existing Like or create a new one.
        # This handles the case where a user tries to like a post multiple times.
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # Only create a notification if the like was newly created.
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked',
                target=post
            )
            return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        Allows a user to unlike a post.
        """
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()`, and `list()` actions for comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically sets the author of a new comment to the current user.
        Also creates a notification for the post's author.
        """
        comment = serializer.save(author=self.request.user)
        # Create a notification for the post's author when a new comment is made.
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented on',
            target=comment.post
        )


class UserFeedView(generics.ListAPIView):
    """
    A view that returns a feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of posts from users the current user follows,
        ordered by creation date.
        """
        # Get the list of users the current user is following using the `following` M2M field.
        following_users = self.request.user.following.all()
        # Filter posts to only include those authored by followed users and the current user
        queryset = Post.objects.filter(Q(author__in=following_users) | Q(author=self.request.user))
        
        # Explicitly order the queryset by the created_at field in descending order
        return queryset.order_by('-created_at')
