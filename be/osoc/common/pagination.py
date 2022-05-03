"""
Pagination for backend.
"""
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    """
    StandardPagination used throughout osoc app.

    Note: no generic views are used, so it is not possible to use
          REST_FRAMEWORK: DEFAULT_PAGINATION_CLASS in settings.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500
