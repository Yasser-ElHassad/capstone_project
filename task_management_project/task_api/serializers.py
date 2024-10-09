from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['created_at', 'updated_at', 'completed_at']
    
    def validat_due_date(self,value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
