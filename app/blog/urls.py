from django.urls import path
from .views import PostListAPIView

app_name="blog"
urlpatterns = [
    path('',PostListAPIView.as_view(),name="list"),
]
