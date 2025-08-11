from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books owned by user1 and user2
        self.book1 = Book.objects.create(
            title="Book One",
            publication_year=2020,
            author=self.author1,
            owner=self.user1
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            publication_year=2021,
            author=self.author2,
            owner=self.user2
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both books returned

    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Book One'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books_by_author_name(self):
        url = reverse('book-list') + '?search=Author Two'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author']['name'], 'Author Two')

    def test_order_books_by_publication_year(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The first book should be the one with the later year (2021)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    def test_retrieve_book_detail(self):
        url = reverse('book-detail', args=[self.book1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2022,
            'author': self.author1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['owner'], self.user1.id)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2022,
            'author': self.author1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_owner(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('book-update', args=[self.book1.pk])
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')

    def test_update_book_not_owner(self):
        self.client.login(username='user2', password='pass123')
        url = reverse('book-update', args=[self.book1.pk])
        data = {
            'title': 'Hacker Update',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_owner(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('book-delete', args=[self.book1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_not_owner(self):
        self.client.login(username='user2', password='pass123')
        url = reverse('book-delete', args=[self.book1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
