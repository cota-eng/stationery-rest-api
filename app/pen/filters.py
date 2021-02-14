from django_filters import rest_framework as filters
from . import models


class PenOriginalFilter(filters.FilterSet):
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
    name = filters.CharFilter(field_name="name", lookup_expr='iexact')
    tag = filters.CharFilter(field_name='tag__slug',lookup_expr='icontains')
    class Meta:
        model = models.Pen
        fields = ('name','tag','brand','price_yen','category',)