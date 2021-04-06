from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryReadOnlyViewSet)
router.register('brand',views.BrandReadOnlyViewSet)
router.register('tag', views.TagReadOnlyViewSet)
"""
below 3 view is not needed
"""
router.register('product-category',views.ProductCategoryFilteredReadOnlyViewSet)
router.register('product-brand',views.ProductBrandFilteredReadOnlyViewSet)
router.register('product-tag', views.ProductTagFilteredReadOnlyViewSet)
# so many query
router.register('search',views.ProductSearchByAllConditions)
router.register('fav',views.FavProductAPIView)
# router.register('products',views.ProductRetrieveView)
router.register('pro',views.ProductPagingReadOnlyViewSet)
router.register('review',views.ReviewViewSet)
# router.register('review-read',views.ReviewReadOnlyViewSet)
app_name="pen"
urlpatterns = [
    path("products/",views.ProductListAPIView.as_view(),name="product-list"),
    path("products/<str:pk>/",views.ProductRetrieveAPIView.as_view(),name="product"),
    path("fav-list/",views.OwnFavProductListAPIView.as_view(),name="fav-list"),
    path("review-list/",views.OwnReviewProductListAPIView.as_view(),name="review-list"),
    path('',include(router.urls)),
]
