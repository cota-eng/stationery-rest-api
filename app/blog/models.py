from django.db import models
from django.contrib.auth import get_user_model
from markdown import markdown,mark_safe
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

    
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

class Comment(models.Model):
    content = models.TextField()
    commentator = models.ForeignKey(
        get_user_model(),
        related_name="commentator",
        on_delete=models.CASCADE
        )
    # parent = 
