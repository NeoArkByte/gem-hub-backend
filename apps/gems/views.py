from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import GemListing
from .serializers import GemListingSerializer
from apps.core.permissions import IsOwner, IsAdminUser
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='status', description='Filter by status (e.g., APPROVED, PENDING, REJECTED)', required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='owner_id', description='Filter by owner profile UUID', required=False, type=OpenApiTypes.UUID),
            OpenApiParameter(name='size', description='Custom client page size override (e.g., 20)', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='page', description='Target pagination page number', required=False, type=OpenApiTypes.INT),
        ]
    )
)

class GemListingViewSet(viewsets.ModelViewSet):
    queryset = GemListing.objects.all()
    serializer_class = GemListingSerializer

    def get_permissions(self):
        """
        Dynamically limits access. Anyone can browse all gems or view a specific gem.
        Everything else (creating, editing, deleting) requires an authenticated token.
        """
        
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner(field_name='owner') | IsAdminUser]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            # Default fallback
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Dynamically filters listings based on URL query parameters.
        Supports case-insensitive status matches and client-specific owner filters.
        """
        queryset = GemListing.objects.all()
        
        status_param = self.request.query_params.get('status')
        owner_param = self.request.query_params.get('owner_id')
        
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
            
        if owner_param:
            queryset = queryset.filter(owner_id=owner_param)
            
        return queryset.order_by('-gem_id')