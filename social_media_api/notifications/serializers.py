"""
This module defines the serializer for the Notification model.
"""
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    """
    # Read-only fields to show details about the actor and target.
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_object = serializers.CharField(source='target.title', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 'is_read', 'timestamp', 'target', 'target_object']
        read_only_fields = ['recipient', 'actor', 'verb', 'timestamp', 'target']
