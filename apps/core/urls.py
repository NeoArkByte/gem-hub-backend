from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet)  # Prefix for the URL
router.register(r"profiles", ProfileViewSet)  # Prefix for the URL

urlpatterns = [
    path("", include(router.urls)),
]
