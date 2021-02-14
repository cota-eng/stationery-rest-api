from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryReadOnlyViewSet)
router.register('pen',views.PenReadOnlyViewSet)
router.register('search',views.PenSearchByAllConditions)
urlpatterns = [
    path('',include(router.urls))
]
