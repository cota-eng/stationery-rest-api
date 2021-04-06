from rest_framework.pagination import PageNumberPagination

class NormalPagination(PageNumberPagination):
    page_size = 5
    # page_size_query_param = 'page_size'
    # max_page_size = 10000

class FilteredResultPagination(PageNumberPagination):
    page_size = 12