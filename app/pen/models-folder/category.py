from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User
import ulid
# from core.models import ULIDField


class Category(models.Model):
    """
    Model that define category and id is normal
    """
    name = models.CharField(
        _("category name"),
        max_length=50,
        unique=True,
        )
    slug = models.CharField(
        _("category slug"),
        max_length=50,
        unique=True,
        )
    
    def __str__(self):
        return f'Category: {self.name}'
