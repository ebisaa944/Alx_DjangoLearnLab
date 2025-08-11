from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # CRUD for Posts
    path('', PostListView.as_view(), name='blog_home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # User Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Comment URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:post_pk>/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    ]