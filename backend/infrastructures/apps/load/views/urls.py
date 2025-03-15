from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoadViewSet

load_router = DefaultRouter()
load_router.register(prefix=r"", viewset=LoadViewSet, basename="load")

load_urlpatterns = [
    path("", include(load_router.urls)),
]
