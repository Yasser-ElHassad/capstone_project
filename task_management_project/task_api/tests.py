from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class UserAPITestCase(TestCase):
    def setUp(self) :
        self.client = APIClient()
        self.user_data = {
            'username':'testuser',
            'email':'test@example.com',
            'password':'testpass123'
        }

        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
    
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user_detail(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': (timezone.now() + timedelta(days=1)).isoformat(),
            'priority': 'MEDIUM',
            'status': 'PENDING'
        }

    def test_create_task(self):
        url = reverse('task-list')
        response = self.client.post(url, self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_get_task_list(self):
        Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_task_detail(self):
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-detail', kwargs={'pk': task.pk})
        updated_data = {
            'title': 'Updated Task',
            'description': 'This task has been updated',
            'due_date': (timezone.now() + timedelta(days=2)).isoformat(),
            'priority': 'HIGH',
            'status': 'PENDING'
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=task.pk).title, 'Updated Task')

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_toggle_complete(self):
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-toggle-complete', kwargs={'pk': task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=task.pk).status, 'COMPLETED')

    def test_filter_tasks(self):
        Task.objects.create(user=self.user, **self.task_data)
        Task.objects.create(user=self.user, title='Another Task',due_date = (timezone.now() + timedelta(days=2)).isoformat(), priority='HIGH', status='COMPLETED')
        url = reverse('task-list')
        
        # Test filtering by status
        response = self.client.get(url, {'status': 'PENDING'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

        # Test filtering by priority
        response = self.client.get(url, {'priority': 'HIGH'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Another Task')

    def test_sort_tasks(self):
        Task.objects.create(user=self.user, **self.task_data)
        Task.objects.create(user=self.user, title='Another Task', priority='HIGH', due_date=timezone.now() + timedelta(days=3))
        url = reverse('task-list')
