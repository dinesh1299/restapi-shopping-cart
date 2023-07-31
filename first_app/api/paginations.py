from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class CustomPagination(PageNumberPagination):
    page_size = 3 
    page_query_param ='records'
    page_size_query_param = 'user_page_size'
    max_page_size = 7
    last_page_strings = ['end']

class CustomLimitsetPagination(LimitOffsetPagination):
    default_limit = 6
    limit_query_param = 'custom_limit'
    offset_query_param = 'custom_offset'
    max_limit = 10

class CustomCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-rating'