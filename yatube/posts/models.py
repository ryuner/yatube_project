from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import BooleanField

user = get_user_model()

class Group(models.Model):
    title = models.TextField()
    slug = models.URLField()
    description = models.TextField()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
    author = models.ForeignKey(
        user, 
        on_delete=models.CASCADE,
        related_name='post'
    ) 
