from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework import permissions
from rest_framework import generics

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    filter_fields = ('slug', )
    lookup_field = 'slug'
        
# class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#     permission_classes = (permissions.AllowAny,)
#     filter_fields = ('slug', )
#     class Meta:
#         lookup_field = 'slug'



# class OwnReviewListView(generics.ListAPIView):
"""View that get data reviewed by request user:IsAuthenticated"""
#     serializer_class = 
#     def get_queryset(self):
#         user = self.request.user
#         return .objects.filter(=user)

# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.
#     permission_classes = (permissions.AllowAny,)
#     class Meta:
#         lookup_field = ''
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)