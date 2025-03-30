from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(default=False) 

    def __str__(self):
        return self.title  
    

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    is_finished = models.BooleanField(default=False) 

    def __str__(self):
        return self.task