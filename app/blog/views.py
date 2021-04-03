from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    PostListSerializer,
)
from .models import (
    Post,
    Comment,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from django.db.models import Q

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["title", "content",]
    
    def get_queryset(self):
        # super(PostListAPIView,self).get_queryset(self)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(titel__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return queryset

class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
