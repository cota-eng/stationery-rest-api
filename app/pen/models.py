from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User
import ulid
from core.models import ULIDField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Category(models.Model):
    """
    Model that define category and id is normal
    """
    name = models.CharField(
        _("category name"),
        max_length=50,
        unique=True,
        )
    slug = models.SlugField(
        _("category slug"),
        max_length=50,
        unique=True,
        )
    
    def __str__(self):
        return f'Category: {self.name}'

class Brand(models.Model):
    """
    Model that define Maker and has name and only one official web site
    """
    name = models.CharField(
        _('brand name'),
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        _("brand slug"),
        unique=True,
        )
    official_site_link = models.URLField(
         _("brand link"),
         max_length=255,
         unique=True
        )

    def __str__(self):
        return f'Brand: {self.name}'

class Tag(models.Model):
    """
    Model that has diffrent tags, such as Wood, Light, Rich, Boys ...
    """
    name = models.CharField(
        _("category name"),
        max_length=50,
        unique=True,
        )
    slug = models.SlugField(
        _("category slug"),
        unique=True,
        )
    
    def __str__(self):
        return f'Tag: {self.name}'


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
        related_name="product",
        # TODO: CASCADE -> SETNULL
        on_delete=models.CASCADE
        )
    price_yen = models.PositiveIntegerField(
        _("price"),
        validators=[MaxValueValidator(1000000),]
        )
    brand = models.ForeignKey(
        Brand,
        related_name="product",
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="product",
    )
    image = ProcessedImageField(
        upload_to='products',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True)
    # in JP 出典
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

    """
    TODO: not needed? this field is able to be impletemted in front end
    """
    # @property
    # def mercari_link_to_buy(self):
    #     return f'https://www.mercari.com/jp/search/?keyword={self.name}'

    # @property
    # def number_of_fav(self):
    #     return self.prefetch_related('faved').count()

    # TODO: thinking of Average (will be ordered by score...)
    # @property
    # def avarage_of_review_star(self):
    #     sum: int = 0
    #     reviews = self.objects.prefetch_related('review').filter(product=self)
    #     if len(reviews) != 0:
    #         for review in reviews:
    #             sum += review.avarage_star
    #         return sum / len(reviews)
    #     else:
    #         return 0
        
    def __str__(self):
        return f'product: {self.name} Price: {self.price_yen}'
    

class FavProduct(models.Model):
    """
    Fav is Favorite
    TODO: user content-type
    {"liked":false,"likable_id":29686,"likable_type":"Article"}
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


class Review(models.Model):

    # def __init__(self, *args, **kwargs):
    #     stars_of_design = self.stars_of_design
    #     stars_of_durability = self.stars_of_durability
    #     stars_of_usefulness = self.stars_of_usefulness
    #     stars_of_function = self.stars_of_function
    #     stars_of_easy_to_get = self.stars_of_easy_to_get
    #     self.stars_list = [
    #         stars_of_design,
    #         stars_of_durability,
    #         stars_of_usefulness,
    #         stars_of_function,
    #         stars_of_easy_to_get,
    #     ]

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
        """
        average of individual star
        """
        stars_list = [
            self.stars_of_design,
            self.stars_of_durability,
            self.stars_of_usefulness,
            self.stars_of_function,
            self.stars_of_easy_to_get,
        ]
        sum = 0
        for star in stars_list:
            sum += star
        return float(sum / len(stars_list))

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
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'product'], name='unique_booking'),
        ]
        indexes = [
            models.Index(fields=['reviewer', 'product'])
        ]
        """
        in the future, cannot use below code
        """
        # unique_together = (('reviewer','product'))
        # index_together = (('reviewer', 'product'))

    def __str__(self):
        return f'Reviewd product: {self.product.name} / Reviewer: {self.reviewer.username}'
    
# class Comment(models.Model):
#     pass