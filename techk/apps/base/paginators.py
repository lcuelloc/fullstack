from rest_framework import pagination
from rest_framework.response import Response

from rest_framework.pagination import CursorPagination


class NumPagesPagination(pagination.PageNumberPagination):
    """
    Data per page from queryset
    """

    page_size_query_param = "page_size"
    page_size = 100
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
            }
        )
