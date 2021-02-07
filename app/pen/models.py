from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from account.models import User
class Category(models.Model):
    """Model that define category and id is normal"""
    name = models.CharField(_("category name"),max_length=50)
    def __str__(self):
        return f'Category: {self.name}'

class Productor(models.Model):
    """Model that define Maker and has name and only one official web site"""
    name = models.CharField(max_length=50)
    official_site_link = models.CharField(max_length=255)
    def __str__(self):
        return f'Productor: {self.name}'

class Tag(models.Model):
    """Model that has diffrent tags, such as Wood, Light, Rich ..."""
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'Tag: {self.name}'

class Pen(models.Model):
    """Model that is main part"""
    name = models.CharField(_("pen name"), max_length=50)
    description = models.TextField(_('description'))
    category = models.ForeignKey(
        _('category'),
        Category,
        related_name="pen_category",
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(
        _("price"),
        validators=[MaxValueValidator(1000000),]
        )
    productor = models.ForeignKey(
        _('productor'),
        Productor,
        related_name="pen_productor",
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        _('tag'),
        Tag,
        related_name="pen_tag",
    )
    image = models.ImageField(
        _("pen images"),
        upload_to=None,
        height_field=None, width_field=None, max_length=None)
    image_src = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    amazon_link_to_buy = models.CharField(blank=True, null=True)
    rakuten_link_to_buy = models.CharField(blank=True, null=True)

    def merukari_link_to_buy(self):
        return f'https://www.mercari.com/jp/search/?keyword={self.name}'

    def __str__(self):
        return f'Pen: {self.name} Price: {self.price_yen}'
    
class Review(models.model):
    pen = models.ForeignKey(
        _('pen'),
        Pen,
        related_name='reviewed_pen',
        on_delete=models.CASCADE)
    stars = models.IntegerField(_('star'), validators=[MaxValueValidator(5), MinValueValidator(1)])
    reviewer = models.ForeignKey(
        _('reviewer'),
        User,
        related_name='reviewer',
        on_delete=models.CASCADE)

    class Meta:
        unique_together = (('reviewer','pen'))
        index_together = (('reviewer', 'pen'))

    def __str__(self):
        return f'Reviewd Pen: {self.pen.name} / Reviewer: {self.user.nickname}'
    