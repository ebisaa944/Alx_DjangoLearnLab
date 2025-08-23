"""
This module defines the views for the posts app, including CRUD operations for
posts and comments, as well as a user-specific feed.
"""
from rest_framework import viewsets, generics, status, permissions
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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically sets the author of a new post to the current user.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Allows a user to like a specific post.
        """
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically sets the author of a new comment to the current user.
        Also creates a notification for the post's author.
        """
        comment = serializer.save(author=self.request.user)
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented on',
            target=comment.post
        )


class UserFeedView(generics.ListAPIView):
    """
    A view that returns a feed of posts from users the current user follows,
    ordered by creation date (most recent first).
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # <- full reference

    def get_queryset(self):
        user = self.request.user
        # Get users the current user follows
        following_users = user.following.all()  # Make sure this M2M exists on your User model

        # Return posts authored by followed users, most recent first
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
