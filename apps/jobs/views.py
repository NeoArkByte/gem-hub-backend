from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.core.permissions import IsOwner, IsAdminUser  # Imported your custom permissions
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer

# 1. Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        """
        Dynamically limits access. Anyone can browse all jobs or view a specific job.
        Everything else (creating, editing, deleting) requires authentication, ownership, or admin rights.
        """
        
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner(field_name='employer') | IsAdminUser]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Job.objects.all()

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 2. Application ViewSet
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        """
        Dynamically limits access for applications. Public read-only, 
        restricted modifications.
        """

        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner(field_name='applicant') | IsAdminUser]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]
