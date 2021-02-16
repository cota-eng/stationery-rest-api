from rest_framework import serializers
from . import models
from account.models import User
from account.serializers import UserSerializer

pen_detail_url = serializers.HyperlinkedIdentityField(
    view_name='pen:pen',
    lookup_field='id'
    )

class CategorySerializer(serializers.ModelSerializer):
    # pen_category = PenSerializer()
    # url = pen_detail_url
    class Meta:
        model = models.Category
        fields = (
            'name',
            'slug',
            'pen_category',
            )
        depth = 1

class BrandSerializer(serializers.ModelSerializer):
    # pen = PenSerializer()
    class Meta:
        model = models.Brand
        fields = (
            'name',
            'slug',
            'official_site_link',
            )
        depth = 1

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = (
            'name',
            'slug',
            'pen_tag',
            )
        depth = 1


class ReviewSerialier(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    reviewer = UserSerializer()
    class Meta:
        model = models.Review
        fields = (
            'title',
            'stars',
            'reviewer',
            'created_at',
            )
        depth = 1
        
class PenSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    category = CategorySerializer()
    brand = BrandSerializer()
    tag = TagSerializer(many=True)
    reviewed_pen = ReviewSerialier(many=True)
    class Meta:
        model = models.Pen
        fields = (
            'pk',
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
            'reviewed_pen'
            )
        # read_only_fields = '__all__'
        depth = 1

    
