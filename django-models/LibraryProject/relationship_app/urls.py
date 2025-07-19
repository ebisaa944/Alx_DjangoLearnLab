from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='relationship_app/logout.html'
    ), name='logout'),
    path('admin/', views.admin_view, name='admin_dashboard'),
    path('librarian/', views.librarian_view, name='librarian_dashboard'),
    path('member/', views.member_view, name='member_dashboard'),
]
