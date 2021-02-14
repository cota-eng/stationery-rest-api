from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class CategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny)
    # filter_fields = ('slug', )
    lookup_field = 'slug'
        
class PenReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Pen.objects.all()
    serializer_class = serializers.PenSerializer
    permission_classes = (permissions.AllowAny,)
    # filter_fields = ('slug',)

from django_filters import rest_framework as filters
from .filters import  PenOriginalFilter

class PenSearchByAllConditions(viewsets.ReadOnlyModelViewSet):
    """
    search like below
    http://localhost:8000/api/search/?name=S20&?price_yen=2000
    """
    queryset = models.Pen.objects.all()
    serializer_class = serializers.PenSerializer
    permission_classes = (permissions.AllowAny,)
    # filter_backends = [filters.DjangoFilterBackend,]
    # filterset_fields = ('name','price_yen','brand',)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PenOriginalFilter


# class PenCategoryFilteredReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.Pen.objects.filter(category=)
#     serializer_class = serializers.CategorySerializer
#     permission_classes = (permissions.AllowAny,)
#     filter_fields = ('slug', )

# class PenBrandFilteredReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.Pen.objects.filter(category=)
#     serializer_class = serializers.CategorySerializer
#     permission_classes = (permissions.AllowAny,)
#     filter_fields = ('slug', )


# class OwnReviewListView(generics.ListAPIView):
"""View that get data reviewed by request user:IsAuthenticated"""
#     serializer_class = 
#     def get_queryset(self):
#         user = self.request.user
#         return .objects.filter(=user)
from rest_framework.decorators import  action
from rest_framework import authentication
# class ReviewViewSet(generics.CreateAPIView):
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [authentication.SessionAuthentication,]
    # permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = ''
    # def perform_create(self, serializer):
    #     serializer.save(reviewer=self.request.user)

    @action(detail=True,methods=["POST"])
    def rate_pen(self, request, pk=None):
        if 'stars' in request.data:
            pen = models.Pen.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                review = models.Review.objects.get(reviewer=user, pen=pen)
                review.stars = stars
                review.save()
                serializer = serializers.ReviewSerialier(review, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                review = models.Review.objects.create(reviewer=user, pen=pen, stars=stars)
                response = {'message': 'created'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'not working'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
