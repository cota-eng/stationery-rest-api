from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    """Model that define category and id is normal"""
    name = models.CharField(_("category name"),max_length=50)
    def __str__(self):
        return self.name

class Productor(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Pen(models.Model):
    name = models.CharField(_("pen's name"), max_length=50)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name="pen_category",
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(
        _("price"),
        validater=[MaxValueValidator(100000),]
        )
    productor = models.ForeignKey(
        Productor,
        related_name="pen_productor",
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="pen_tag",
        on_delete=models.CASCADE
    )
    image=models.ImageField(_("pen's images"), upload_to=None, height_field=None, width_field=None, max_length=None)