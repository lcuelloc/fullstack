from django.urls import path, include

from rest_framework import routers

from apps.categories.views import CategoryListView

router_category = routers.SimpleRouter()
router_category.register(r"categories", CategoryListView, base_name="category")

urlpatterns = []

# -- Admin Urls
urlpatterns += [
    path("", include(router_category.urls)),
]
