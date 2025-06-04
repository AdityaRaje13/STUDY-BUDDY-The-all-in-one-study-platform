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
    
    
class Study_Group(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='study_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Post(models.Model):
    community_id = models.CharField(max_length=50, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_post')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=50)
    attached_file = models.FileField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def upvote_count(self):
        return self.upvotes.count()  # Count upvotes for this post
    
    

class Upvote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Ensure a user can only upvote a post once

    def __str__(self):
        return f"{self.user.username} upvoted {self.post.title}"
    

