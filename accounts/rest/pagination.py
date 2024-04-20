# from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    page_size = 5
    page_size_query_param = 'offset'
    limit_query_param = 'offset'
    offset_query_param = 'start'
    max_page_size = 100


# class CustomDatatablesPageNumberPagination(DatatablesPageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100
