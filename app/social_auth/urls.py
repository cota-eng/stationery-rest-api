from django.urls import path
from . import views

app_name='social_auth'
urlpatterns = [
    path('google/',views.GoogleAuthView.as_view(),name='google-login')
]
