
from .views import admin_view
from .views import member_view
from .views import librarian_view
from .views import list_books
from .views import logout_view
from .views import login_view
from .views import register_view
from .views import LibraryDetailView
from django.urls import path

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]
