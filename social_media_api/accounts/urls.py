"""
This module defines the URL patterns for the accounts app, including user registration, login, and follow/unfollow actions.
"""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, UserLoginView, FollowUser, UnfollowUser

urlpatterns = [
    # URL for user registration.
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # URL for user login.
    path('login/', UserLoginView.as_view(), name='user-login'),
    # URL for following a user. The <int:pk> captures the user's ID.
    path('follow/<int:pk>/', FollowUser.as_view(), name='follow-user'),
    # URL for unfollowing a user. The <int:pk> captures the user's ID.
    path('unfollow/<int:pk>/', UnfollowUser.as_view(), name='unfollow-user'),
]
