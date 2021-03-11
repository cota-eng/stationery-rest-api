from rest_framework import serializers
from . import models
from authentication.models import User
from authentication.serializers import UserSerializer

class FavSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)
    lookup_field = 'faved.pk'
    class Meta:
        model = models.Fav
        fields = '__all__'
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'name',
            'slug',
            'product_category',
            )
        # depth = 1


class CategoryUsingProductSerializer(serializers.ModelSerializer):
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
            )
        # depth = 1

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
            'product_tag',
            )
        # depth = 1

class TagUsingPenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = (
            'name',
            'slug',
            )
        # depth = 1


class ReviewSerialier(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    """
    reviewer - avatar, nickname, id
    """
    reviewer = UserSerializer(read_only=True)
    class Meta:
        model = models.Review
        fields = (
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
        depth = 1

import markdown

class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d", read_only=True)
    category = CategoryUsingProductSerializer()
    brand = BrandSerializer()
    tag = TagUsingPenSerializer(many=True)
    review = ReviewSerialier(many=True)
    # description = serializers.SerializerMethodField()

    # def get_description(self, instance):
    #     return markdown.markdown(instance.description)
    
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
            'review'
            )
        # read_only_fields = '__all__'
        depth = 1

    
