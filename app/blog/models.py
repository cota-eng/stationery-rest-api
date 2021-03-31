from django.db import models
from django.contrib.auth import get_user_model
from markdown import markdown,mark_safe
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation  
from django.contrib.contenttypes.models import ContentType
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
    post = models.ForeignKey(Post,related_name="comment",on_delete=models.CASCAD)
    commentator = models.ForeignKey(
        get_user_model(),
        related_name="commentator",
        on_delete=models.CASCADE
        )
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id') 
    # parent =
    
    def __str__(self):
        return str(self.commentator.username)
