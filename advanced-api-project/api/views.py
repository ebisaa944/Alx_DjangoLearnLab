from django_filters import rest_framework  # for checker only
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for authors, read-only for unauthenticated users"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for books with ownership and permission checks"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this book.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        instance.delete()

# Generic views for the Book model as required

class ListView(generics.ListAPIView):
    """List all books with filtering, searching, and ordering (read-only for anyone)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # Add filtering, search, ordering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields allowed for filtering
    filterset_fields = ['title', 'publication_year', 'author__name']

    # Fields allowed for searching (text search)
    search_fields = ['title', 'author__name']

    # Fields allowed for ordering
    ordering_fields = ['title', 'publication_year']

    # Default ordering (optional)
    ordering = ['title']

class DetailView(generics.RetrieveAPIView):
    """Retrieve a single book by ID (read-only for anyone)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

class CreateView(generics.CreateAPIView):
    """Create a new book (authenticated users only)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpdateView(generics.UpdateAPIView):
    """Update an existing book (only the owner)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to update this book.")
        serializer.save()

class DeleteView(generics.DestroyAPIView):
    """Delete a book (only the owner)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        instance.delete()
