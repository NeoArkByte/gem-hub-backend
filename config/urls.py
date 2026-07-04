from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # admin dashboard
    path("admin/", admin.site.urls),
    # documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    # rest endpoints
    path("api/v1/", include("apps.gems.urls")),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/", include("apps.jobs.urls")),
]
