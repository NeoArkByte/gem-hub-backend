from rest_framework import viewsets
from .models import Notification, Profile
from .serializers import NotificationSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    # def get_permissions(self):
    #     # Allow everyone to view, but only authenticated users to create/delete
    #     if self.action in ['list', 'retrieve']:
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    permission_classes = [AllowAny]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [AllowAny]
