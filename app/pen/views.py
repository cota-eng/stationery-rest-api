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
from .filters import  ProductOriginalFilter,OwnFavFilter
from rest_framework import pagination
from rest_framework import mixins
from rest_framework import generics

class FilteredResultPagination(pagination.PageNumberPagination):
    page_size = 12

# class FilteredResultPagination(pagination.LimitOffsetPagination):
#     default = 2
#     max_limit = 10

class FavProductAPIView(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    get specific fav info
    EX
    endpoint:http://localhost:8000/api/fav/?fav_user=01F02WMKMEP7AMQ859595GEK37&product=01EYZ0NBPVP428BF7ZERHBEQVH
    """
    queryset = models.Fav.objects.all()
    serializer_class = serializers.FavSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OwnFavFilter
    """
    below is return single obj...
    """
    # lookup_field = "product"
    # lookup_url_kwarg = "fav_user"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    # def get(self, request, pk=None):
    #     """
    #     fav/fav_id/ => get is_favorite
    #     """
    #     queryset = self.get_queryset()
    #     serializer = serializers.FavSerializer
    #     return Response(serializer.data)
  
    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def fav(self, request, pk=None):
        """
        FAV
        default false
        if not faved => fav
        product = models.Product.objects.get(id=pk)
        user:self.request.user => bool true

        UNFAV
        if faved => not faved
        user:self.request.user => bool false

        """
        product = models.Product.objects.get(id=pk)
        # productのid入手
        user = request.user
        # get_or_create
        try:
            fav = models.Fav.objects.get(fav_user=user.pk, product=product)
            if fav.is_favorite:
                fav.is_favorite = False
            else:
                fav.is_favorite = True
            fav.save()
            serializer = serializers.FavSerializer(fav, many=False)
            response = {'message': 'Rating updated', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except models.Fav.DoesNotExist:
            fav = models.Fav.objects.create(
                fav_user=user,
                product=product,
                is_favorite=True,
                )
            response = {'message': 'first faved'}
            return Response(response, status=status.HTTP_200_OK)
     
    # def destroy(self, request, *args, **kwargs):
    #     """
    #     delete is invalid
    #     """
    #     response = {'message': 'DELETE method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     """
    #     put is invalid
    #     """
    #     response = {'message': 'PUT method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     patch is invalid
    #     """
    #     response = {'message': 'PATCH method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryReadOnlyViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    for list category view \n
    display category related product !
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'
        
class ProductReadOnlyViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.AllowAny,)
    # lookup_field = 'slug'

class TagReadOnlyViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    for list tag view \n
    display tag related product !
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

class BrandReadOnlyViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    for list brand view \n
    display brand related product !
    """
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

class ProductSearchByAllConditions(mixins.ListModelMixin,
                                   viewsets.GenericViewSet):
    """
    search like below \n
    http://localhost:8000/api/search/?name=S20&? \n
    all condition searching
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.AllowAny,)
    # pagination_class = FilteredResultPagination
    # pagination_class = pagination.LimitOffsetPagination
    # add &?limit=100&offset=500
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductOriginalFilter

# class PenCategoryFilteredReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.Pen.objects.filter(category=)
#     serializer_class = serializers.CategorySerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     filter_fields = ('slug', )

class ProductBrandFilteredReadOnlyViewSet(mixins.ListModelMixin,
                                          viewsets.GenericViewSet):
    """
    filter by brand/<brand_name_slug>
    display Respective Brand Pens !
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        slug = self.request.GET.get('slug')
        return self.queryset.filter(brand__slug=slug)

class ProductCategoryFilteredReadOnlyViewSet(mixins.ListModelMixin,
                                             viewsets.GenericViewSet):
    """
    filter by brand/<category_name_slug>
    display Respective Category Products !
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        slug = self.request.GET.get('slug')
        return self.queryset.filter(category__slug=slug)


class ProductTagFilteredReadOnlyViewSet(mixins.ListModelMixin,
                                        viewsets.GenericViewSet):
    """
    filter by tag
    display Respective Tag Products !
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        slug = self.request.GET.get('slug')
        return self.queryset.filter(tag__slug=slug)

class OwnReviewViewSet(viewsets.ModelViewSet):
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
    @action(detail=True,methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def rate(self, request, pk=None):
        if 'title' in request.data:
            product = models.Product.objects.get(id=pk)
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
                review = models.Review.objects.get(reviewer=user, product=product)
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
            except models.Review.DoesNotExist:
                review = models.Review.objects.create(
                    reviewer=user,
                    product=product,
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