from django_filters import rest_framework as filters
from . import models


class OwnFavFilter(filters.FilterSet):
    """
    
    """
    fav_user = filters.CharFilter(field_name="fav_user", lookup_expr='exact')
    # product = filters.CharFilter(field_name='product',lookup_expr='exact')
    class Meta:
        model = models.Fav
        fields = ('fav_user',)
        
class ProductOriginalFilter(filters.FilterSet):
    """
    price - less than equal
            more than equal
    name - contains
    tag - contains
    brand - exact (multi choice)
    category - exact (one choice why emits so many resuts)
    """
    lte = filters.NumberFilter(field_name='price_yen', lookup_expr='lte')
    gte = filters.NumberFilter(field_name='price_yen', lookup_expr='gte')
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    tag = filters.CharFilter(field_name='tag__slug',lookup_expr='exact')
    class Meta:
        model = models.Product
        fields = ('name','tag','brand','category',)