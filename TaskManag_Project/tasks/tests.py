from django.test import TestCase
from rest_framework.test import APIRequestFactory

# Create your tests here.
# factory = APIRequestFactory()
# request = factory.post('/notes/', {'title':'new idea'})

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book

class BookApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(user=self.user)
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2022
        )
        
        self.book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023
        }
        
        self.url = reverse('book-list')

    def test_create_book(self):
        response = self.client.post(self.url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(title='New Book').author, 'New Author')

    def test_get_book_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        updated_data = {'title': 'Updated Book', 'author': 'Updated Author', 'publication_year': 2024}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        Book.objects.create(title='Django Book', author='Django Author', publication_year=2021)
        response = self.client.get(f"{self.url}?title=Django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django Book')

    def test_search_books(self):
        Book.objects.create(title='Python Programming', author='Python Author', publication_year=2020)
        response = self.client.get(f"{self.url}?search=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Programming')

    def test_order_books(self):
        Book.objects.create(title='A Book', author='A Author', publication_year=2019)
        response = self.client.get(f"{self.url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book')  # 2022 comes before 2019

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)