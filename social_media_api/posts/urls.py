# posts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers # The corrected import
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

# Nested router for comments
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post' )
posts_router.register(r'comments', CommentViewSet, basename='post-comments' )

urlpatterns = [
    path('', include(router.urls) ),
    path('', include(posts_router.urls)),
]