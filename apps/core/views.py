from rest_framework import viewsets
from .models import Notification, Profile
from .serializers import NotificationSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwner

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        """
        Even with ModelViewSet, this creates a data fortress.
        Users can only pull queries where they are the recipient.
        """
        # If testing in a view or unauthenticated state, return none safely
        if self.request.user.is_anonymous:
            return Notification.objects.none()
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    def get_permissions(self):
        """
        Dynamically limits access. Modifying, creating, or deleting requires being logged in AND the recipient.
        """

        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
            
        return [permission() for permission in permission_classes]

            



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """
        Dynamically limits access. Anyone can browse all profiles or view a specific profile.
        Everything else (creating, editing, deleting, or fetching by owner) requires a token.
        """
        
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner(field_name='id') | IsAdminUser]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsOwner(field_name='id') | IsAdminUser]
        else:
            # Default fallback
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]

            

