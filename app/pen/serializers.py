from rest_framework import serializers
from . import models
from authentication.models import User
# from authentication.serializers import UserSerializer
from django.contrib.auth import get_user_model
from authentication.models import User
import markdown


class ReviewerSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    # twitter_account = serializers.ReadOnlyField(source="profile.twitter_account")
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
            # 'email': {
            #     'read_only':True
            # },
        }

class ProductInFavListSerializer(serializers.ModelSerializer):
    # category = CategoryUsingProductSerializer(read_only=True)
    # brand = BrandSerializer(read_only=True)
    # tag = TagUsingPenSerializer(many=True,read_only=True)
    class Meta:
        model = models.Product
        fields = ('id',
                  'name',
                #   'price_yen',
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
    # created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)
    # lookup_field = 'faved.pk'
    class Meta:
        model = models.FavProduct
        fields = ('is_favorite','fav_user','product',)
        read_only_fields = ('is_favorite','fav_user','product',)
    
class FavUsedInProfileSerializer(serializers.ModelSerializer):
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
        # ex read_only_fields = ('name',)
        # depth = 1


class CategoryForProductSerialier(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'id',
            'name',
            )
        # depth = 1

class BrandSerializer(serializers.ModelSerializer):
    # pen = PenSerializer()
    class Meta:
        model = models.Brand
        fields = (
            'id',
            'name',
            'slug',
            'official_site_link',
            'product'
            )
        # depth = 1
        
class BrandForProductSerializer(serializers.ModelSerializer):
    # pen = PenSerializer()
    class Meta:
        model = models.Brand
        fields = (
            'id',
            'name',
            'slug',
            'official_site_link',
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
            'mercari_link_to_buy',
            'number_of_review',
            'avarage_of_review_star',
            # 'reviewed_pen'
            )
        # depth = 1

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = (
            'name',
            'slug',
            'product',
            )
        # depth = 1

class TagUsingPenSerializer(serializers.ModelSerializer):
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
        # depth = 1


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


class ProductSerializer(serializers.ModelSerializer):
    """
    serializer - BrandForProductSerializer,CategoryForProductSerialier

    """
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    category = CategoryForProductSerialier(read_only=True)
    brand = BrandForProductSerializer(read_only=True)
    tag = TagUsingPenSerializer(many=True,read_only=True)
    review = ReviewSerialier(many=True)
    
    # for rate action, many = false is must
    # description = serializers.SerializerMethodField()
    
    @property
    def get_description(self, instance):
        return markdown.markdown(instance.description)
    
    @staticmethod
    def setup_for_query(queryset):
        """
        to many - tag, review
        to one  - category, brand

        reviwew - filter each product...
        """
        queryset = queryset.prefetch_related('tag','review__reviewer','review__reviewer__profile','review__reviewer__profile__avatar','review__product',)
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
                  'mercari_link_to_buy',
                  'number_of_review',
                  'avarage_of_review_star',
                  'review',
                  'created_at',
                  'updated_at',
                  'category',
                  'brand',
                  'tag',)
        read_only_fields = (
                'id',
                'name',
                'description',
                'price_yen',
                'image',
                'image_src',
                'amazon_link_to_buy',
                'rakuten_link_to_buy',
                'mercari_link_to_buy',
                'number_of_review',
                'avarage_of_review_star',
            )
        depth = 1

    
