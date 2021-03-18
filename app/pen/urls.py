from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryReadOnlyViewSet)
router.register('products',views.ProductReadOnlyViewSet)
router.register('search',views.ProductSearchByAllConditions)
router.register('review',views.ReviewViewSet)
router.register('review-read',views.ReviewReadOnlyViewSet)
router.register('tag',views.TagReadOnlyViewSet)
router.register('my-review',views.OwnReviewReadOnlyViewSet)
router.register('brand',views.ProductBrandFilteredReadOnlyViewSet)
router.register('fav',views.FavProductAPIView)
app_name="pen"
urlpatterns = [
    path('',include(router.urls))
]
