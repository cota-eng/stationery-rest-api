from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('user',views.UserReadOnlyViewSet)
router.register('profile',views.OwnProfileListRetrieveUpdateViewSet)


urlpatterns = [
    path('login/',views.GoogleLogin.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
