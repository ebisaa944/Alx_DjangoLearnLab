# posts/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        # Order posts by creation date in descending order (most recent first)
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Like(models.Model):
    """
    Represents a user liking a post.
    """
    # The user who liked the post.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    # The post that was liked.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    # A timestamp for when the like was created.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only like a post once.
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'