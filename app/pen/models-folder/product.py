from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User
import ulid
from core.models import ULIDField
from .category import Category
from .brand import Brand
from .tag import Tag
from .review import  Review


class Product(models.Model):
    """Model that is main part"""
    id = ULIDField(
        primary_key=True,
        default=ulid.new,
        unique=True,
        editable=False,
        db_index=True
        )
    name = models.CharField(
        _("name"), max_length=50)
    # TODO: markdown -> html field
    description = models.TextField(
        _('description'))
    category = models.ForeignKey(
        Category,
        related_name="product_category",
        # TODO CASCADE -> SETNULL
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(
        _("price"),
        validators=[MaxValueValidator(1000000),]
        )
    brand = models.ForeignKey(
        Brand,
        related_name="product_brand",
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="product_tag",
    )
    image = models.ImageField(
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True)
    image_src = models.CharField(
        blank=True,
        null=True,
        max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    """
    in the future, set affiliate link, so is charfield
    """
    amazon_link_to_buy = models.CharField(
        blank=True,
        null=True,
        max_length=500)
    rakuten_link_to_buy = models.CharField(
        blank=True,
        null=True,
        max_length=500)

    @property
    def mercari_link_to_buy(self):
        return f'https://www.mercari.com/jp/search/?keyword={self.name}'

    @property
    def number_of_review(self):
        reviews = Review.objects.filter(product=self)
        return len(reviews)

    # TODO:アベレージ考え中
    @property
    def avarage_of_review_star(self):
        sum: int = 0
        reviews = Review.objects.filter(product=self)
        if len(reviews) != 0:
            for review in reviews:
                sum += review.avarage_star
            return sum / len(reviews)
        else:
            return 0
        
    def __str__(self):
        return f'product: {self.name} Price: {self.price_yen}'
    