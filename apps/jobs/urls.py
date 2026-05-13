from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, JobViewSet

router = DefaultRouter()
router.register(r"jobs", JobViewSet)
router.register(r"applications", ApplicationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
