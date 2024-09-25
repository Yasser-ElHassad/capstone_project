from django.urls import path
from .views import TaskListCreateAPIView

urlpatterns = [
    path('api/tasks/', TaskListCreateAPIView.as_view(), name='task_list_create')
]