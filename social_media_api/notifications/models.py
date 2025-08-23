"""
This module defines the Notification model for the social media API.
"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class Notification(models.Model):
    """
    Represents a notification sent to a user.
    Uses GenericForeignKey to link to any model instance (e.g., Post, Comment).
    """
    # The user who receives the notification.
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    # The user who performed the action that triggered the notification.
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    # A short description of the action (e.g., 'liked', 'commented on', 'followed').
    verb = models.CharField(max_length=255)
    # Boolean to track if the notification has been read.
    is_read = models.BooleanField(default=False)
    # The timestamp of the notification.
    timestamp = models.DateTimeField(auto_now_add=True)

    # GenericForeignKey to the object that the notification is about (the 'target').
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target} - to {self.recipient.username}'