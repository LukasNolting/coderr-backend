from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom paginator to handle invalid pages gracefully.
    """
    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            self.page = None
            return []

    def get_paginated_response(self, data):
        if self.page is None:
            return Response({
                'detail': 'Ungültige Seite. Automatisch auf Seite 1 zurücksetzen.',
                'invalid_page': True,
            }, status=200)

        return super().get_paginated_response(data)