"""
This module defines the URL patterns for the notifications app.
"""
from django.urls import path
from .views import NotificationListView

urlpatterns = [
    # URL for a user to view their notifications
    path('', NotificationListView.as_view(), name='notification-list'),
]