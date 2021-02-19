from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import  action
from rest_framework import authentication
from django_filters import rest_framework as filters
from .filters import  PenOriginalFilter

class AddFavPenAPIView(generics.GenericAPIView):
    pass

class CategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
        
class PenReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Pen.objects.all()
    serializer_class = serializers.PenSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = 'slug'

class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

class PenSearchByAllConditions(viewsets.ReadOnlyModelViewSet):
    """
    search like below
    http://localhost:8000/api/search/?name=S20&?
    all condition searching
    """
    queryset = models.Pen.objects.all()
    serializer_class = serializers.PenSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PenOriginalFilter


# class PenCategoryFilteredReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.Pen.objects.filter(category=)
#     serializer_class = serializers.CategorySerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     filter_fields = ('slug', )

class PenBrandFilteredReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    filter by brand/<brand_name_slug>
    display Respective Brand Pens !
    """
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    # def get_queryset(self):
    #     return self.queryset.filter(slug=self.request.GET.get('slug'))
    # def retrieve(self, request, pk=None):
    #     response = {'message': 'retrieve method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

class OwnReviewReadOnlyViewSet(viewsets.ModelViewSet):
    """
    View that get data reviewed by request user:IsAuthenticated
    """
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return models.Review.objects.filter(reviewer=user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = ''
    # permission_classes = (permissions.IsAuthenticated,)
    # def perform_create(self, serializer):
    #     serializer.save(reviewer=self.request.user)
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return serializers.RecipeDetailSerializer
    #     elif self.action == 'upload_image':
    #         return serializers.RecipeImageSerializer
    @action(detail=True,methods=["POST"])
    def rate_pen(self, request, pk=None):
        if 'stars' in request.data:
            pen = models.Pen.objects.get(id=pk)
            stars = request.data['stars']
            title = request.data['title']
            user = request.user
            try:
                review = models.Review.objects.get(reviewer=user, pen=pen)
                review.stars = stars
                review.title = title
                review.save()
                serializer = serializers.ReviewSerialier(review, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                review = models.Review.objects.create(reviewer=user, pen=pen, stars=stars,title=title)
                response = {'message': 'created'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'not working'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        delete is invalid
        """
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        put is invalid
        """
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        patch is invalid
        """
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)