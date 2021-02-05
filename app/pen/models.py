from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    """Model that define category and id is normal"""
    name = models.CharField(_("category name"),max_length=20)
    def __str__(self):
        return self.name

class Productor(models.Model):
    """Model that define Maker and has name"""
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Tag(models.Model):
    """Model that has diffrent tags, such as Wood, Light, Rich ..."""
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Pen(models.Model):
    """Model that is main part"""
    name = models.CharField(_("pen's name"), max_length=50)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name="pen_category",
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(
        _("price"),
        validators=[MaxValueValidator(100000),]
        )
    productor = models.ForeignKey(
        Productor,
        related_name="pen_productor",
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="pen_tag",
    )
    image = models.ImageField(_("pen's images"), upload_to=None, height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    