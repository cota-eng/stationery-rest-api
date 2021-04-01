from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class PostLimitOffsetPagination(LimitOffsetPagination):
    default = 5
    max_limit = 10