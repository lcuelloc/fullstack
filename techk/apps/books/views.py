from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.books.models import Book
from apps.books.serializers import BookSerializer

from apps.base.paginators import NumPagesPagination


class BookView(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    - List all books.
    - Delete all books
    - Get one book
    - Update one book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []
    authentication_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category', 'upc', 'title', 'price', 'stock']
    # pagination_class = NumPagesPagination

    @action(methods=["post"], detail=False, permission_classes=[])
    def bulk_delete(self, request, pk=None):
        """
        Bulk delete by UPC list
        """
        qs = self.filter_queryset(self.get_queryset())
        upc_list = request.data.get('upc_list', [])
        qs.filter(upc__in=upc_list).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
