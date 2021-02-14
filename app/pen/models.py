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
    slug = models.CharField(_("category slug"),max_length=50)
    def __str__(self):
        return f'Category: {self.name}'

class Brand(models.Model):
    """Model that define Maker and has name and only one official web site"""
    name = models.CharField(max_length=50)
    slug = models.CharField(_("category slug"),max_length=50)
    official_site_link = models.CharField(max_length=255)
    def __str__(self):
        return f'Productor: {self.name}'

class Tag(models.Model):
    """Model that has diffrent tags, such as Wood, Light, Rich, Boys ..."""
    name = models.CharField(max_length=50)
    slug = models.CharField(_("category slug"),max_length=50)
    def __str__(self):
        return f'Tag: {self.name}'

class Pen(models.Model):
    #  short_uuid = models.UUIDField(
    #     _('uuid'),
    #     primary_key=True,
    #     default=str(uuid.uuid4)[:8],
    #     editable=False,
    #     db_index=True) 
    """Model that is main part"""
    name = models.CharField(
        _("name"), max_length=50)
    # TODO markdown -> html field
    description = models.TextField(
        _('description'))
    category = models.ForeignKey(
        Category,
        related_name="pen_category",
        # TODO CASCADE -> SETNULL
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(
        _("price"),
        validators=[MaxValueValidator(1000000),]
        )
    brand = models.ForeignKey(
        Brand,
        related_name="pen_brand",
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="pen_tag",
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
        reviews = Review.objects.filter(pen=self)
        return len(reviews)

    # アベレージ考え中
    @property
    def avarage_of_review_star(self):
        sum: int = 0
        reviews = Review.objects.filter(pen=self)
        if len(reviews) != 0:
            for review in reviews:
                sum += review.stars
            return sum / len(reviews)
        else:
            return 0
        
    def __str__(self):
        return f'Pen: {self.name} Price: {self.price_yen}'
    
class Review(models.Model):
    """Model that display reviews of pens"""
    pen = models.ForeignKey(
        Pen,
        related_name='reviewed_pen',
        on_delete=models.CASCADE)
    """
    review - 買いやすさ、デザイン、使いやすさ、壊れにくさ、疲れにくさ、あともう一個、で総合的な評価とする
                comprehensive_starsとする。
                avarage自体どうするか
                個人のアベレージを取るのと、個人のアベレージを平均したものをペンのトップに載せる

                レビュー自体は1,2,3,4,5だが、平均のみfloatで扱う

    レビュー自体が参考になったか：きちんとしたレビューは評価され、みんなにより見てもらう必要がある
    """
    title = models.CharField(_('title'), max_length=30)
    stars = models.IntegerField(_('star'), validators=[MaxValueValidator(5), MinValueValidator(1)])
    reviewer = models.ForeignKey(
        User,
        related_name='reviewer',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        """
        one review for one person 
        """
        unique_together = (('reviewer','pen'))
        index_together = (('reviewer', 'pen'))

    def __str__(self):
        return f'Reviewd Pen: {self.pen.name} / Reviewer: {self.user.nickname}'
    
# class Comment(models.Model):
#     pass