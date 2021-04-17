from rest_framework import serializers
from .models import (
    Category,
    Product,
    Brand,
    Tag,
    FavProduct,
    Review,
)
from authentication.models import User
from django.contrib.auth import get_user_model
from authentication.models import User
import markdown
from pen.models import Product

class CategoryForProductSerialier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'slug',
            'name',
            )

class BrandForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'slug',
            'official_site_link',
            )


class TagForProductSerializer(serializers.ModelSerializer):
    @staticmethod
    def setup_for_query(queryset):
        queryset = queryset.select_related('product')
        return queryset

    class Meta:
        model = Tag
        fields = (
            'name',
            'slug',
            )



class ProductListSerializer(serializers.ModelSerializer):
    """
    For Listing Product
    """
    category = CategoryForProductSerialier(read_only=True)
    brand = BrandForProductSerializer(read_only=True)
    tag = TagForProductSerializer(many=True,read_only=True)
    number_of_review = serializers.SerializerMethodField()
    number_of_fav = serializers.SerializerMethodField()


    def get_number_of_review(self,instance):
        return instance.review.count()

    def get_number_of_fav(self,instance):
        return instance.faved.count()

    @staticmethod
    def setup_for_query(queryset):
        """
        to many - tag, review, fav
        to one  - category, brand
        reviwew - filter each product...
        """
        queryset = queryset.prefetch_related(
            'tag', 'review__reviewer', 'review__reviewer__profile', 'review__reviewer__profile__avatar', 'review__product', 'faved', 'category'
            )
        queryset = queryset.select_related('category','brand')
        return queryset

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'price',
                  'image',
                  'number_of_review',
                  'category',
                  'brand',
                  'tag',
                  'number_of_fav',
                  )


class ReviewerSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField()
    # @staticmethod
    # def setup_for_query(queryset):
    #     queryset = queryset.select_related('profile')
    #     return queryset
    
    def get_avatar(self, obj):
        avatar = obj.profile.avatar
        if avatar:
            return avatar.name
        return None

    def get_nickname(self, obj):
        return obj.profile.nickname

    class Meta:
        model = User
        fields = ('id','profile','nickname','avatar',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

# class ProductInFavListSerializer(serializers.ModelSerializer):
#     """
#     used in fav-list - ok
#     """
#     # category = CategoryUsingProductSerializer(read_only=True)
#     # brand = BrandSerializer(read_only=True)
#     # tag = TagForProductSerializer(many=True,read_only=True)
#     class Meta:
#         model = models.Product
#         fields = ('id',
#                   'name',
#                   'image',
#                 #   'number_of_review',
#                 #   'avarage_of_review_star',
#                 #   'category',
#                 #   'brand',
#                 #   'tag',
#                   )
#         read_only_fields = (
#                 'id',
#                 'name',
#                 # 'price',
#                 'image',
#                 # 'image_src',
#                 # 'amazon_link_to_buy',
#                 # 'rakuten_link_to_buy',
#                 # 'mercari_link_to_buy',
#                 # 'number_of_review',
#                 # 'avarage_of_review_star',
#             )

class FavProductSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = FavProduct
        fields = ('is_favorite','fav_user','product',)
        read_only_fields = ('is_favorite','fav_user','product',)
    
class OwnFavListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    class Meta:
        model = FavProduct
        fields = ('product',)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'product',
            )



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'slug',
            'official_site_link',
            'product'
            )
        

class BrandFilteredProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'category',
            'price',
            'brand',
            'tag',
            'image',
            'image_src',
            'created_at',
            'updated_at',
            'amazon_link_to_buy',
            'rakuten_link_to_buy',
            'number_of_review',
            'avarage_of_review_star',
            )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
            'slug',
            'product',
            )



class ReviewNotIncludeUserSerialier(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    """
    reviewer - avatar, nickname, id
    """
    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'stars_of_design',
            'stars_of_durability',
            'stars_of_usefulness',
            'stars_of_function',
            'stars_of_easy_to_get',
            'avarage_star',
            'good_point_text',
            'bad_point_text',
            'created_at',
            )

class ReviewSerialier(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    """
    reviewer - avatar, nickname, id
    """
    reviewer = ReviewerSerializer(read_only=True)


    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'stars_of_design',
            'stars_of_durability',
            'stars_of_usefulness',
            'stars_of_function',
            'stars_of_easy_to_get',
            'avarage_star',
            'good_point_text',
            'bad_point_text',
            'reviewer',
            'created_at',
            )
        """
        TODO: validation add!
        """
        extra_kwargs = {
            "title": {
                'max_length':100,
            }
        }


class OwnReviewProductListSerialier(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    """
    reviewer - avatar, nickname, id
    """
    # reviewer = ReviewerSerializer(read_only=True)

    @staticmethod
    def setup_for_query(queryset):
        """
        to many - tag, review
        to one  - category, brand
        reviwew - filter each product...
        """
        queryset = queryset.prefetch_related()
        queryset = queryset.select_related()
        return queryset

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'stars_of_design',
            'stars_of_durability',
            'stars_of_usefulness',
            'stars_of_function',
            'stars_of_easy_to_get',
            'avarage_star',
            'good_point_text',
            'bad_point_text',
            'reviewer',
            'created_at',
            )
        """
        TODO: validation add!
        """
        extra_kwargs = {
            "title": {
                'max_length':100,
            }
        }


class RelatedProductListSerializer(serializers.ModelSerializer):
    """
    For Listing Product
    """
    category = CategoryForProductSerialier(read_only=True)
    brand = BrandForProductSerializer(read_only=True)
    # tag = TagForProductSerializer(many=True,read_only=True)
    # number_of_review = serializers.SerializerMethodField()
    # number_of_fav = serializers.SerializerMethodField()


    # def get_number_of_review(self,instance):
    #     return instance.review.count()

    # def get_number_of_fav(self,instance):
    #     return instance.faved.count()

    @staticmethod
    def setup_for_query(queryset):
        """
        to many - tag, review, fav
        to one  - category, brand
        reviwew - filter each product...
        """
        queryset = queryset.prefetch_related(
            'tag',
            # 'review__reviewer',
            # 'review__reviewer__profile',
            # 'review__reviewer__profile__avatar',
            # 'review__product',
            # 'faved',
            'category'
            )
        queryset = queryset.select_related('category','brand')
        return queryset

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'image',
                #   'number_of_review',
                #   'number_of_fav',
                  'category',
                  'brand',
                #   'tag',
                  )

class ProductRetrieveSerializer(serializers.ModelSerializer):
    """
    serializer - BrandForProductSerializer,CategoryForProductSerialier

    """
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    category = CategoryForProductSerialier(read_only=True)
    brand = BrandForProductSerializer(read_only=True)
    tag = TagForProductSerializer(many=True,read_only=True)
    review = ReviewSerialier(many=True)
    number_of_review = serializers.SerializerMethodField()
    # description = serializers.SerializerMethodField()
    number_of_fav = serializers.SerializerMethodField()

    related = RelatedProductListSerializer(source="related_products",many=True)

    def get_number_of_review(self,instance):
        return instance.review.count()

    def get_number_of_fav(self,instance):
        return instance.faved.count()

    """
    TODO:時間ができたら文章入力していくため、今はmarkdownでなくていい
    """
    # def get_description(self, instance):
    #     return markdown.markdown(instance.description)


    @staticmethod
    def setup_for_query(queryset):
        """
        to many - tag, review
        to one  - category, brand
        reviwew - filter each product...
        """
        queryset = queryset.prefetch_related(
            'tag',
            'review__reviewer',
            'review__reviewer__profile',
            'review__reviewer__profile__avatar',
            'review__product',
            'related_products__category',
            'related_products__brand',
            'related_products__tag',
            )
        queryset = queryset.select_related('category','brand')
        return queryset

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'image',
            'image_src',
            'amazon_link_to_buy',
            'rakuten_link_to_buy',
            'number_of_review',
            'review',
            'created_at',
            'updated_at',
            'category',
            'brand',
            'tag',
            'number_of_fav',
            'related',
            #   "related_products",
            )