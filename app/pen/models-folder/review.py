from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User
import ulid
from core.models import ULIDField

from .product import  Product

class Review(models.Model):
    """Model that display reviews of pens"""
    id = ULIDField(
        primary_key=True,
        default=ulid.new,
        unique=True,
        editable=False,
        db_index=True
        )
    product = models.ForeignKey(
        Product,
        related_name='review',
        on_delete=models.CASCADE)
    """
    TODO:
    avarage自体どうするか
    個人のアベレージと、個人のアベレージを平均したものをペンのトップに載せる
    レビュー自体が参考になったか：きちんとしたレビューは評価され、みんなにより見てもらう必要がある
    """
    title = models.CharField(_('title'), max_length=30)
    """
    TODO: 
    デザイン性
    耐久性
    利便性
    機能性
    入手性
    """
    stars_of_design = models.IntegerField(
        _('design'),
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    stars_of_durability = models.IntegerField(
        _('durability'),
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    stars_of_usefulness = models.IntegerField(
        _('usefulness'),
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    stars_of_function = models.IntegerField(
        _('function'),
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    stars_of_easy_to_get = models.IntegerField(
        _('easy_to_get'),
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )

    @property
    def avarage_star(self):
        sum = 0
        sum += self.stars_of_design
        sum += self.stars_of_durability
        sum += self.stars_of_usefulness
        sum += self.stars_of_function
        sum += self.stars_of_easy_to_get
        return float(sum / 5)

    good_point_text = models.TextField(blank=True,null=True)
    bad_point_text = models.TextField(blank=True,null=True)
    reviewer = models.ForeignKey(
        User,
        related_name='reviewer',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        """
        one review for one person 
        """
        unique_together = (('reviewer','product'))
        index_together = (('reviewer', 'product'))

    def __str__(self):
        return f'Reviewd product: {self.product.name} / Reviewer: {self.reviewer.nickname}'
    