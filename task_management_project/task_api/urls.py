from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('',include(router.urls))
]