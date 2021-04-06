from rest_framework import serializers
from . import models
from authentication.models import User
# from authentication.serializers import UserSerializer
from django.contrib.auth import get_user_model
from authentication.models import User
import markdown

class CategoryForProductSerialier(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'id',
            'slug',
            'name',
            )

class BrandForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
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
        model = models.Tag
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
        model = models.Product
        fields = ('id',
                  'name',
                  'price_yen',
                  'image',
                  'number_of_review',
                  'category',
                  'brand',
                  'tag',
                  'number_of_fav',
                  )
        read_only_fields = (
                'id',
                'name',
                'description',
                'price_yen',
                'image',
                'image_src',
                'number_of_fav,'
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

class ProductInFavListSerializer(serializers.ModelSerializer):
    """
    used in fav-list - ok
    """
    # category = CategoryUsingProductSerializer(read_only=True)
    # brand = BrandSerializer(read_only=True)
    # tag = TagForProductSerializer(many=True,read_only=True)
    class Meta:
        model = models.Product
        fields = ('id',
                  'name',
                  'image',
                #   'number_of_review',
                #   'avarage_of_review_star',
                #   'category',
                #   'brand',
                #   'tag',
                  )
        read_only_fields = (
                'id',
                'name',
                # 'price_yen',
                'image',
                # 'image_src',
                # 'amazon_link_to_buy',
                # 'rakuten_link_to_buy',
                # 'mercari_link_to_buy',
                # 'number_of_review',
                # 'avarage_of_review_star',
            )

class FavProductSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.FavProduct
        fields = ('is_favorite','fav_user','product',)
        read_only_fields = ('is_favorite','fav_user','product',)
    
class OwnFavListSerializer(serializers.ModelSerializer):
    product = ProductInFavListSerializer()
    class Meta:
        model = models.FavProduct
        fields = ('product',)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'name',
            'slug',
            'product',
            )



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = (
            'id',
            'name',
            'slug',
            'official_site_link',
            'product'
            )
        

class BrandFilteredProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            'id',
            'name',
            'description',
            'category',
            'price_yen',
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
        model = models.Tag
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
        model = models.Review
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
        model = models.Review
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
        model = models.Review
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
    description = serializers.SerializerMethodField()
    number_of_fav = serializers.SerializerMethodField()

    def get_number_of_review(self,instance):
        return instance.review.count()

    def get_number_of_fav(self,instance):
        return instance.faved.count()

    def get_description(self, instance):
        return markdown.markdown(instance.description)
    
    @staticmethod
    def setup_for_query(queryset):
        """
        to many - tag, review
        to one  - category, brand
        reviwew - filter each product...
        """
        queryset = queryset.prefetch_related(
            'tag', 'review__reviewer', 'review__reviewer__profile', 'review__reviewer__profile__avatar', 'review__product',
            )
        queryset = queryset.select_related('category','brand')
        return queryset

    class Meta:
        model = models.Product
        fields = ('id',
                  'name',
                  'description',
                  'price_yen',
                  'image',
                  'image_src',
                  'amazon_link_to_buy',
                  'rakuten_link_to_buy',
                  'number_of_review',
                #   'avarage_of_review_star',
                  'review',
                  'created_at',
                  'updated_at',
                  'category',
                  'brand',
                  'tag',
                  'number_of_fav',
                  )
        read_only_fields = (
                'id',
                'name',
                'description',
                'price_yen',
                'image',
                'image_src',
                'amazon_link_to_buy',
                'rakuten_link_to_buy',
                'number_of_fav,'
            )



    
