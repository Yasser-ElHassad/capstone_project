from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    options = {
        'L':'Low',
        'M':'Medium',
        'H':'High'
    }
    statu = {
        'P':'Pending',
        'L':'In Progress',
        'C':'Completed',
    }
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    due_date = models.DateTimeField()
    priority_level = models.CharField(max_length=10, choices=options)
    status = models.CharField(max_length=10, choices=statu)


class Users(models.Model):
    username  = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
