from django.urls import path
from .views import BookList, BookListCreate, BookRetrieveUpdateDestroy

urlpatterns = [
    # This meets the basic requirement
    path('books/', BookList.as_view(), name='book-list-basic'),
    
    # These provide enhanced functionality
    path('books/advanced/', BookListCreate.as_view(), name='book-list-create'),
    path('books/advanced/<int:pk>/', BookRetrieveUpdateDestroy.as_view(), name='book-detail'),
]
