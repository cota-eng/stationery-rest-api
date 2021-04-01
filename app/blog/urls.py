from django.urls import path
from .views import (
    PostListAPIView,
    PostDetailAPIView,
)

app_name="blog"
urlpatterns = [
    path('post/',PostListAPIView.as_view(),name="list"),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name="list"),
]
