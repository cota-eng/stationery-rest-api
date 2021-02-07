from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name','slug',)
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Productor
        fields = ('name', 'slug', 'official_site_link',)
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name', 'slug',)
        depth = 1
        
class PenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pen
        fields = ('name', 'description','category', 'price_yen', 'productor', 'tag', 'image', 'image_src', 'created_at', 'updated_at', 'amazon_link_to_buy', 'rakuten_link_to_buy', )
        read_only_fields=('image_src','created_at','updated_at')
        
    
class ReviewSerialier(serializers.ModelSerializer):
    def create(self):
        