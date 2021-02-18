from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User

class Category(models.Model):
    """
    Model that define category and id is normal
    """
    name = models.CharField(
        _("category name"),
        max_length=50)
    slug = models.CharField(
        _("category slug"),
        max_length=50)
    
    def __str__(self):
        return f'Category: {self.name}'

class Brand(models.Model):
    """
    Model that define Maker and has name and only one official web site
    """
    name = models.CharField(
        _('brand name'),
        max_length=50)
    slug = models.CharField(
        _("brand slug"),
        max_length=50)
    official_site_link = models.CharField(
         _("brand link"),
         max_length=255)

    def __str__(self):
        return f'Productor: {self.name}'

class Tag(models.Model):
    """
    Model that has diffrent tags, such as Wood, Light, Rich, Boys ...
    """
    name = models.CharField(
        _("category name"),
        max_length=50)
    slug = models.CharField(
        _("category slug"),
        max_length=50)
    
    def __str__(self):
        return f'Tag: {self.name}'

class Pen(models.Model):
    """Model that is main part"""
    # id = models.UUIDField(
    #     _('uuid'),
    #     primary_key=True,
    #     default=str(uuid.uuid4)[:8],
    #     editable=False,
    #     db_index=True) 
    name = models.CharField(
        _("name"), max_length=50)
    # TODO: markdown -> html field
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

    # TODO:アベレージ考え中
    @property
    def avarage_of_review_star(self):
        sum: int = 0
        reviews = Review.objects.filter(pen=self)
        if len(reviews) != 0:
            for review in reviews:
                sum += review.avarage_star
            return sum / len(reviews)
        else:
            return 0
        
    def __str__(self):
        return f'Pen: {self.name} Price: {self.price_yen}'
    

class FavPen(models.Model):
    """
    Fav is Favorite
    """
    # is_favorite = models.BooleanField(default=False)
    """
    TODO:
    connect to User or Profile
    """
    fav_user = models.ForeignKey(
        User,
        related_name="user_fav",
        on_delete=models.CASCADE
    )
    pen = models.ForeignKey(
        Pen,
        related_name="pen_fav",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """
        one review for one person 
        """
        unique_together = (('fav_user','pen'))
        index_together = (('fav_user', 'pen'))
    def __str__(self):
        return f"stock {self.pen.name} user {self.fav_user}"

class Review(models.Model):
    """Model that display reviews of pens"""
    pen = models.ForeignKey(
        Pen,
        related_name='reviewed_pen',
        on_delete=models.CASCADE)
    """
    TODO:
    avarage自体どうするか
    個人のアベレージと、個人のアベレージを平均したものをペンのトップに載せる
    レビュー自体が参考になったか：きちんとしたレビューは評価され、みんなにより見てもらう必要がある
    """
    title = models.CharField(_('title'), max_length=30)
    # stars = models.IntegerField(
    #     _('star'), validators=[MaxValueValidator(5), MinValueValidator(1)]
    #     )
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
        unique_together = (('reviewer','pen'))
        index_together = (('reviewer', 'pen'))

    def __str__(self):
        return f'Reviewd Pen: {self.pen.name} / Reviewer: {self.reviewer.user_profile.nickname}'
    
# class Comment(models.Model):
#     pass