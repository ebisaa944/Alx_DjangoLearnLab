from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet, BookListCreate, BookRetrieveUpdateDestroy

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')


urlpatterns = [
    # This meets the basic requirement
    path('books/', BookList.as_view(), name='book-list-basic'),
    
    # These provide enhanced functionality
    path('books/advanced/', BookListCreate.as_view(), name='book-list-create'),
    path('books/advanced/<int:pk>/', BookRetrieveUpdateDestroy.as_view(), name='book-detail'),

     # Include all router-generated URLs
    path('', include(router.urls)),  # This line must be exactly like this
]
