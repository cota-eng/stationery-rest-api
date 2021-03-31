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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    is_exist = qs.exists()
    if is_exist:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug
    

def pre_save_post_reciewver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

class CommentManager(models.Manager):

    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager,self).filter(content_type=content_type,object_id=obj_id)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

    

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
    objects = CommentManager()
    parent = models.ForeignKey("self",null=True,blank=True)
    
    
    def __str__(self):
        return str(self.commentator.username)
    
    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True