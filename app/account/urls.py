from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
app_name="account"
urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('email-veryfy/',views.EmailVerifyAPIView.as_view(),name="email-veryfy"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token-refresh"),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPIView.as_view(),name="password-reset-check"),
    # path('password-reset/<uidb64>/<token>/',views.PasswordResetAPIView.as_view(),name="password-reset-check"),
]
