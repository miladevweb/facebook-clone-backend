from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    # ?page=3&page_size=6