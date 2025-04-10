from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExtractViewSet

extract_router = DefaultRouter()
extract_router.register(prefix=r"", viewset=ExtractViewSet, basename="extract")


extract_urlpatterns = [
    path("", include(extract_router.urls)),
]
