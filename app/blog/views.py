from rest_framework import generics
from .serializers import (
    PostListSerializer,
)
from .models import (
    Post,
)
from rest_framework.filters import (
    SearchFilter,
    # OrderingFilter,
)

# from django.db.models import Q
from rest_framework.permissions import AllowAny


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [SearchFilter]
    search_fields = ["title", "content", ]

    # def get_queryset(self):
    #     # super(PostListAPIView,self).get_queryset(self)
    #     query = self.request.GET.get("q")
    #     qs = self.queryset
    #     if query:
    #         qs.filter(
    #             Q(titel__icontains=query) |
    #             Q(content__icontains=query)
    #         ).distinct()
    #     return qs
