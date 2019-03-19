from django.urls import path, include
from rest_framework import routers

from .views import GenerateScrapeView


urlpatterns = [
    path("scrape/create/", GenerateScrapeView.as_view())
]
