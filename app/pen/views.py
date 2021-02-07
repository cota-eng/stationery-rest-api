from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework import permissions
class CategoryViewSets(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    class Meta:
        lookup_field = 'slug'
        

