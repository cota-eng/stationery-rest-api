from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User
import ulid
from core.models import ULIDField
from .product import Product

class Fav(models.Model):
    """
    Fav is Favorite
    """
    is_favorite = models.BooleanField(default=False)
    """
    TODO:
    connect to User or Profile
    """
    fav_user = models.ForeignKey(
        User,
        related_name="fav",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name="faved",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """
        one review for one person 
        """
        unique_together = (('fav_user','product'))
        index_together = (('fav_user', 'product'))
        ordering = ['-created_at']

    def __str__(self):
        return f"stock {self.product.name} user {self.fav_user.username}"
