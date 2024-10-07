from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class TaskListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    query = Task.objects.all()
    serializer_class = TaskSerializer