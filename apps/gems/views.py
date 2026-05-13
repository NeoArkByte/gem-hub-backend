from rest_framework import viewsets
from .models import GemListing
from .serializers import GemListingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class GemListingViewSet(viewsets.ModelViewSet):
    queryset = GemListing.objects.all()
    serializer_class = GemListingSerializer

    permission_classes = [AllowAny]

