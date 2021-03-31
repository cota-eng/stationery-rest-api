from django.db import models
from django.contrib.auth import get_user_model
from markdown import markdown,mark_safe

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager,self).filter(is_public=True).filter(pub)


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

    class Meta:
        ordering = ["-published_at"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    # @property
    # def get_content_type(self):
    #     instance = self
    #     content_type = ContentType.objects.get_for_model(instance.__class__)
    #     return content_type


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Post.objects.filter(slug=slug).order_by("-id")
    


class Comment(models.Model):
    content = models.TextField()
    commentator = models.ForeignKey(
        get_user_model(),
        related_name="commentator",
        on_delete=models.CASCADE
        )
    # parent = 
