from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryReadOnlyViewSet)
router.register('brand',views.BrandReadOnlyViewSet)
router.register('tag',views.TagReadOnlyViewSet)
router.register('product-category',views.ProductCategoryFilteredReadOnlyViewSet)
router.register('product-brand',views.ProductBrandFilteredReadOnlyViewSet)
router.register('product-tag',views.ProductTagFilteredReadOnlyViewSet)
router.register('search',views.ProductSearchByAllConditions)
router.register('fav',views.FavProductAPIView)
router.register('products',views.ProductReadOnlyViewSet)
router.register('pro',views.ProductPagingReadOnlyViewSet)
router.register('review',views.ReviewViewSet)
# router.register('review-read',views.ReviewReadOnlyViewSet)
router.register('my-review',views.OwnReviewViewSet)
app_name="pen"
urlpatterns = [
    path("fav-list/",views.ReturnFavProductAPIView.as_view(),name="fav-list"),
    path('',include(router.urls))
]
