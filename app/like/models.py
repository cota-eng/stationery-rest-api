from django.db import models
from django.conf import settings
from pen.models import Product
from blog.models import Post


class Like(models.Model):
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_like",
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class LikeProduct(Like):
    product = models.ForeignKey(
        Product,
        related_name="like",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'product'))
        index_together = (('user', 'product'))
        ordering = ['-created_at']
        # proxy = True

    def __str__(self):
        return f"stock {self.product.name} "


class LikePost(Like):

    post = models.ForeignKey(
        Post,
        related_name="like",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'))
        index_together = (('user', 'post'))
        ordering = ['-created_at']
        # proxy = True

    def __str__(self):
        return f"stock {self.post.title} "
