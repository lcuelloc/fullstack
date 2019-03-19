from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, viewsets

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
    pagination_class = NumPagesPagination
