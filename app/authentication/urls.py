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
app_name="authentication"
router = DefaultRouter()
router.register('user',views.UserReadOnlyViewSet)
router.register('profile',views.OwnProfileListRetrieveUpdateViewSet)
router.register('allprofile',views.ProfileReadOnlyViewSet)
router.register('whoami',views.WhoAmIView)

# router.register('avatar',views.AvatarRetrieveUpdateView)

urlpatterns = [
    path('login/',views.GoogleLogin.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
