from django.urls import path, include

from rest_framework import routers

from apps.books.views import BookView

router_book = routers.SimpleRouter()
router_book.register(r"books", BookView, base_name="book")

urlpatterns = []

# -- Admin Urls
urlpatterns += [
    path("", include(router_book.urls)),
]
