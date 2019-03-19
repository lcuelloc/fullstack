from rest_framework import filters, mixins, viewsets

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class CategoryListView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    - List all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    authentication_classes = []

