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
from rest_framework import pagination

class AddFavPenAPIView(generics.GenericAPIView):
    pass

class CategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'
        
class PenReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Pen.objects.all()
    serializer_class = serializers.PenSerializer
    permission_classes = (permissions.AllowAny,)
    # lookup_field = 'slug'

class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

class FilteredResultPagination(pagination.PageNumberPagination):
    page_size = 12

# class FilteredResultPagination(pagination.LimitOffsetPagination):
#     default = 2
#     max_limit = 10

class PenSearchByAllConditions(viewsets.ReadOnlyModelViewSet):
    """
    search like below
    http://localhost:8000/api/search/?name=S20&?
    all condition searching
    """
    queryset = models.Pen.objects.all()
    serializer_class = serializers.PenSerializer
    permission_classes = (permissions.AllowAny,)
    # pagination_class = FilteredResultPagination
    # pagination_class = pagination.LimitOffsetPagination
    # add &?limit=100&offset=500
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
    permission_classes = (permissions.AllowAny,)
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

class ReviewReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (permissions.AllowAny,)
    

class ReviewViewSet(viewsets.ModelViewSet):
    """
    can review specific pen 
    only authenticateed user 

    """
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = ''
    # def perform_create(self, serializer):
    #     serializer.save(reviewer=self.request.user)
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return serializers.RecipeDetailSerializer
    #     elif self.action == 'upload_image':
    #         return serializers.RecipeImageSerializer
    @action(detail=True,methods=["POST"])
    def rate_pen(self, request, pk=None):
        if 'title' in request.data:
            pen = models.Pen.objects.get(id=pk)
            title = request.data['title']
            stars_of_design = request.data['stars_of_design']
            stars_of_durability = request.data['stars_of_durability']
            stars_of_usefulness = request.data['stars_of_usefulness']
            stars_of_function = request.data['stars_of_function']
            stars_of_easy_to_get = request.data['stars_of_easy_to_get']
            good_point_text = request.data['good_point_text']
            bad_point_text = request.data['bad_point_text']
            user = request.user
            try:
                review = models.Review.objects.get(reviewer=user, pen=pen)
                review.title = title
                review.stars_of_design = stars_of_design
                review.stars_of_durability = stars_of_durability
                review.stars_of_usefulness = stars_of_usefulness
                review.stars_of_function = stars_of_function
                review.stars_of_easy_to_get = stars_of_easy_to_get
                review.good_point_text = good_point_text
                review.bad_point_text = bad_point_text
                review.save()
                serializer = serializers.ReviewSerialier(review, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                review = models.Review.objects.create(
                    reviewer=user,
                    pen=pen,
                    title=title,
                    stars_of_design=stars_of_design,
                    stars_of_durability=stars_of_durability,
                    stars_of_usefulness=stars_of_usefulness,
                    stars_of_function=stars_of_function,
                    stars_of_easy_to_get=stars_of_easy_to_get,
                    good_point_text=good_point_text,
                    bad_point_text=bad_point_text
                    )
                response = {'message': 'review created'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'error evoled'}
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