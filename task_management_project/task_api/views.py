from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        due_date = self.request.query_params.get('due_date')
        sort_by = self.request.query_params.get('sort_by')

        if status:
            queryset = queryset.filter(status=status.upper())
        if priority:
            queryset = queryset.filter(priority=priority.upper())
        if due_date:
            queryset = queryset.filter(due_date__date=due_date)
        
        if sort_by:
            if sort_by.lower() == 'due_date':
                queryset = queryset.order_by('due_date')
            elif sort_by.lower() == 'priority':
                queryset = queryset.order_by('priority')

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'PENDING':
            task.status = 'COMPLETED'
            task.completed_at = timezone.now()
        else:
            task.status = 'PENDING'
            task.completed_at = None
        task.save()
        return Response(TaskSerializer(task).data)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status == 'COMPLETED':
            return Response({"detail":"Completed tasks cannot be edited."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)