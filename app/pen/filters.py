from django_filters import rest_framework as filters
from . import models
class PenOriginalFilter(filters.FilterSet):
    lte = filters.NumberFilter(field_name='price_yen', lookup_expr='lte')
    gte = filters.NumberFilter(field_name='price_yen', lookup_expr='gte')
    
    class Meta:
        model = models.Pen
        fields = ('price_yen',)