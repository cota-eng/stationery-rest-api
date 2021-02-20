from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryReadOnlyViewSet)
router.register('pen',views.PenReadOnlyViewSet)
router.register('search',views.PenSearchByAllConditions)
router.register('review',views.ReviewViewSet)
router.register('tag',views.TagReadOnlyViewSet)
router.register('my-review',views.OwnReviewReadOnlyViewSet)
router.register('brand',views.PenBrandFilteredReadOnlyViewSet)
app_name="pen"
urlpatterns = [
    path('',include(router.urls))
]
