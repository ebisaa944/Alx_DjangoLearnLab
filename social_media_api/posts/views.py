"""
This module defines the views for the posts app, including CRUD operations for
posts and comments, as well as a user-specific feed.
"""
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action


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
        """
        serializer.save(author=self.request.user)


class UserFeedView(generics.ListAPIView):
    """
    A view that returns a feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of posts from users the current user follows,
        ordered by creation date.
        """
        # Get the list of users the current user is following
        following_users = self.request.user.following.all()

        # Only include posts by followed users, ordered by most recent
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
