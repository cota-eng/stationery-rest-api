from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
app_name="account"
urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('email-veryfy/',views.EmailVerifyView.as_view(),name="email-veryfy")
]
