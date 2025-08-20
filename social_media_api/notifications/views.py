"""
This module defines the views for the notifications app.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    A view that returns a list of notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of all notifications for the current user, ordered by timestamp.
        """
        # Get the notifications for the authenticated user.
        queryset = Notification.objects.filter(recipient=self.request.user)
        # Order by timestamp with unread notifications showing first.
        return queryset.order_by('-timestamp')
