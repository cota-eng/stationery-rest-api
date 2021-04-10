from rest_framework import viewsets
from . import serializers
from . import models
from .permissions import IsOwnerOrReadOnly
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
from django.db.models import Q
import environ
env = environ.Env()
env.read_env('.env')
import requests, json
from .pagination import NormalPagination

from django.db.models import  Q

class ProductCategorisedAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    # pagination_class = NormalPagination
    def get_queryset(self):
        # if self.kwargs['category__slug'] is None:
        #     return None
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs.filter(category__slug=self.kwargs['category__slug']).filter(brand__slug=self.kwargs['brand__slug'])

class ProductBrandFilteredAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = NormalPagination
    def get_queryset(self):
        # if self.kwargs['category__slug'] is None:
        #     return None
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs.filter(brand__slug=self.kwargs['brand__slug'])

class OwnFavProductListAPIView(generics.ListAPIView):
    queryset = models.FavProduct.objects.all()
    serializer_class = serializers.OwnFavListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # pagination_class = NormalPagination

    def get_queryset(self):
        # below two code is equal in sql...
        # return self.queryset.filter(Q(fav_user=self.request.user)&Q(is_favorite=True))
        return self.queryset.prefetch_related('product').select_related('fav_user').filter(fav_user=self.request.user).filter(is_favorite=True)

class FavProductAPIView(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,#TODO in production, not needed?
                           viewsets.GenericViewSet):
    """
    get specific fav info
    EX
    endpoint:http://localhost:8000/api/fav/?fav_user=01F02WMKMEP7AMQ859595GEK37&product=01EYZ0NBPVP428BF7ZERHBEQVH
    """
    queryset = models.FavProduct.objects.all()
    serializer_class = serializers.FavProductSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)

    # def get_queryset(self):
    #     return self.queryset.filter(fav_user=self.request.user)
        
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = OwnFavFilter
    """
    below is return single obj...
    """
    # lookup_field = "product"
    # lookup_url_kwarg = "fav_user"
  
    @action(detail=True, methods=["GET"], permission_classes=[permissions.IsAuthenticated])
    def check(self, request, pk=None):
        product = models.Product.objects.get(id=pk)
        user = self.request.user
        try:
            fav = models.FavProduct.objects.get(Q(fav_user__exact=user) & Q(product__exact=product))
        except models.FavProduct.DoesNotExist:
            response = {'message': 'not faved'}
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.FavProductSerializer(fav, many=False)
        response = {'message': 'Fav cheked', 'result': serializer.data["is_favorite"]}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated,IsOwnerOrReadOnly])
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
        # TODO: get_or_create is better?
        try:
            fav = models.FavProduct.objects.get(fav_user=user.pk, product=product)
            if fav.is_favorite:
                fav.is_favorite = False
                fav.save()
                serializer = serializers.FavProductSerializer(fav, many=False)
                response = {'message': 'unfaved', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                fav.is_favorite = True
                fav.save()
                serializer = serializers.FavProductSerializer(fav, many=False)
                response = {'message': 'faved', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        except models.FavProduct.DoesNotExist:
            fav = models.FavProduct.objects.create(
                fav_user=user,
                product=product,
                is_favorite=True,
                )
            response = {'message': 'first faved'}
            return Response(response, status=status.HTTP_200_OK)
     
class OwnReviewProductListAPIView(generics.ListAPIView):
    """
    View that get data reviewed by request user:IsAuthenticated
    """
    queryset = models.Review.objects.all()
    serializer_class = serializers.OwnReviewProductListSerialier
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        user = self.request.user
        return qs.filter(reviewer=user)

        
class ProductPagingReadOnlyViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    for testing
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductRetrieveSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = NormalPagination

class ProductListAPIView(generics.ListAPIView):
    """
    For listing product API
    """
    queryset = models.Product.objects.all()
    # serializer_class = serializers.ProductListSerializer
    serializer_class = serializers.ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    # pagination_class = NormalPagination

    
    def get_queryset(self):
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs
    


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    """
    For product retrieve API
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductRetrieveSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs
    # lookup_field = 'slug'

class CategoryFilteredListAPIView(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    for list category view \n
    display category related product !
    """
    queryset = models.Category.objects.all().prefetch_related("product")
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    # lookup_field = 'slug'

class TagFilteredProductListAPIView(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    for list tag view \n
    display tag related product !
    """
    queryset = models.Tag.objects.all().prefetch_related("product")
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'


class BrandFliteredListAPIView(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    for list brand view \n
    display brand related product !
    """
    queryset = models.Brand.objects.all().prefetch_related("product")
    serializer_class = serializers.BrandSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

# from rest_framework import filters
class ProductSearchByAllConditions(mixins.ListModelMixin,
                                   viewsets.GenericViewSet):
    """
    search like below \n
    http://localhost:8000/api/search/?name=S20&? \n
    all condition searching
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductOriginalFilter
    def get_queryset(self):
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs
    # pagination_class = FilteredResultPagination
    # pagination_class = pagination.LimitOffsetPagination
    # add &?limit=100&offset=500


class ReviewViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    can review specific pen 
    only authenticateed user 
    """
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerialier
    permission_classes = (permissions.AllowAny,)
    # lookup_field = ''
    # def perform_create(self, serializer):
    #     serializer.save(reviewer=self.request.user)
    @action(detail=True,methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def create_review(self, request, pk=None):
        """
        review specific pen 
        ex) http://localhost:8000/api/review/<int:product_id>/create_review/
        """
        if 'title' in request.data:
            product = models.Product.objects.get(id=pk)
            """
            TODO: リスト内包表記で単純化、行数減らす
            """
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
                review.stars_of_design = int(stars_of_design)
                review.stars_of_durability = int(stars_of_durability)
                review.stars_of_usefulness = int(stars_of_usefulness)
                review.stars_of_function = int(stars_of_function)
                review.stars_of_easy_to_get = int(stars_of_easy_to_get)
                review.good_point_text = good_point_text
                review.bad_point_text = bad_point_text
                review.save()
                serializer = serializers.ReviewSerialier(review, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_CREATE_USER")
                requests.post(WEB_HOOK_URL, data = json.dumps({
                    'text': f':smile_cat:Review Updated by {user} !!',  
                }))
                return Response(response, status=status.HTTP_200_OK)
            except models.Review.DoesNotExist:
                review = models.Review.objects.create(
                    reviewer=user,
                    product=product,
                    title=title,
                    stars_of_design=int(stars_of_design),
                    stars_of_durability=int(stars_of_durability),
                    stars_of_usefulness=int(stars_of_usefulness),
                    stars_of_function=int(stars_of_function),
                    stars_of_easy_to_get=int(stars_of_easy_to_get),
                    good_point_text=good_point_text,
                    bad_point_text=bad_point_text
                    )
                response = {'message': 'review created'}
                WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_CREATE_USER")
                requests.post(WEB_HOOK_URL, data = json.dumps({
                    'text': f':smile_cat:Review Created by {user} !!',  
                }))
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'error evoled'}
            WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_CREATE_USER")
            requests.post(WEB_HOOK_URL, data = json.dumps({
                'text': f':smile_cat:Review Failed by {user} !!',  
            }))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

# class ProductBrandFilteredReadOnlyViewSet(mixins.ListModelMixin,
#                                           viewsets.GenericViewSet):
#     """
#     filter by brand/<brand_name_slug>
#     display Respective Brand Pens !
#     """
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductListSerializer
#     permission_classes = (permissions.AllowAny,)
#     def get_queryset(self):
#         slug = self.request.GET.get('slug')
#         return self.queryset.filter(brand__slug=slug)


# class ProductCategoryFilteredReadOnlyViewSet(mixins.ListModelMixin,
#                                              viewsets.GenericViewSet):
#     """
#     filter by brand/<category_name_slug>
#     display Respective Category Products !
#     """
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductListSerializer
#     permission_classes = (permissions.AllowAny,)
#     def get_queryset(self):
#         slug = self.request.GET.get('slug')
#         return self.queryset.filter(category__slug=slug)


# class ProductTagFilteredReadOnlyViewSet(mixins.ListModelMixin,
#                                         viewsets.GenericViewSet):
#     """
#     filter by tag
#     display Respective Tag Products !
#     """
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductListSerializer
#     permission_classes = (permissions.AllowAny,)
#     def get_queryset(self):
#         slug = self.request.GET.get('slug')
#         return self.queryset.filter(tag__slug=slug)


    