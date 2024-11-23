from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class using the PageNumberPagination style.

    Attributes:
        page_size (int): The default number of items per page.
        page_size_query_param (str): The query parameter name to specify a custom page size.
        max_page_size (int): The maximum number of items allowed per page.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500

class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom pagination class using the LimitOffsetPagination style.

    Attributes:
        default_limit (int): The default number of items returned if no limit is specified.
        limit_query_param (str): The query parameter name to specify the limit.
        offset_query_param (str): The query parameter name to specify the starting offset.
        max_limit (int): The maximum number of items that can be returned in a single request.
    """
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
