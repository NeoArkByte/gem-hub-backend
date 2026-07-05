from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"profiles", ProfileViewSet, basename="profile")  # Prefix for the URL

urlpatterns = [
    path("", include(router.urls)),
]
