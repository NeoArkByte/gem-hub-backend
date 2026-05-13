from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GemListingViewSet

router = DefaultRouter()
router.register(r"gems", GemListingViewSet)  # Prefix for the URL

urlpatterns = [
    path("", include(router.urls)),
]
