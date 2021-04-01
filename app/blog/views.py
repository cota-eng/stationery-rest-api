from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    PostListSerializer,
)
from .models import (
    Post,
    Comment,
)



class PostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()

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
