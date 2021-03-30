from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(
        get_user_model(),
        related_name="author",
        on_delete=models.CASCADE
        )
    published_at = models.DateTimeField(auto_now_add=True)
    

class Comment(models.Model):
    pass