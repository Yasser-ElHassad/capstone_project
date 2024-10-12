from django.urls import path, include
from .views import TaskListCreateAPIView, TaskViewSet
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register(r'my-models', TaskViewSet, basename='tasks')


urlpatterns = [
    path('api/', include(route.urls)),
    path('api/tasks/', TaskListCreateAPIView.as_view(), name='task_list_create')
]