from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name','slug',)
        depth = 1

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ('name', 'slug', 'official_site_link',)
        depth = 1

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name', 'slug',)
        depth = 1

        
class PenSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    category = CategorySerializer()
    brand = BrandSerializer()
    tag = TagSerializer()
    # reviewed_pen = ReviewSerialier()
    
    class Meta:
        model = models.Pen
        fields = ('name', 'description','category', 'price_yen', 'brand', 'tag', 'image', 'image_src', 'created_at', 'updated_at', 'amazon_link_to_buy', 'rakuten_link_to_buy', )
        read_only_fields = '__all__'
        
    
class ReviewSerialier(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ('pen', 'stars','reviewer',)
        depth = 1
    
