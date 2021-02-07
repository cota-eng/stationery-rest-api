from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryViewSets)
urlpatterns = [
    path('category/',include(router.urls))
]
