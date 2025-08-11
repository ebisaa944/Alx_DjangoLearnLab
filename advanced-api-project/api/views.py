from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing and editing authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing and editing books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
