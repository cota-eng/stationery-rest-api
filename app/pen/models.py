from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    """Model that define category and id is normal"""
    name = models.CharField(_("category name"),max_length=50)
    def __str__(self):
        return self.name


class Pen(models.Model):
    name = models.CharField(_("pen's name"), max_length=50)
    category = models.ForeignKey(
        Category,
        related_name="pen_category",
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(_("price"),validater=[MaxValueValidator(100000),])
    description = models.TextField()
    # shop
    # productor
    image=models.ImageField(_("pen's images"), upload_to=None, height_field=None, width_field=None, max_length=None)