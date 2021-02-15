from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
router.register('my-profile',views.MyProfileView)
app_name="account"
urlpatterns = [
    path('', include(router.urls)),
    # path('profile/',views.MyProfileView.as_view(),name="profile"),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/',views.LogoutAPIView.as_view(),name="logout"),
    path('email-veryfy/',views.EmailVerifyAPIView.as_view(),name="email-veryfy"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token-refresh"),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPIView.as_view(),name="password-reset-confirm"),
    path('password-reset/',views.PasswordResetAPIView.as_view(),name="password-reset"),
    path('reset-password-complete/',views.SetNewPasswordAPIView.as_view(),name="reset-password-complete"),
]
