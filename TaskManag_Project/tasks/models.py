from django.db import models


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

