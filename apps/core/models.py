from django.db import models
import uuid

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    # 1. Internal Primary Key (UUID)
    # Django will generate this automatically for every new row.
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    # 2. Supabase Auth Link
    # This matches the ID in Supabase Auth (auth.users.id).
    profile_id = models.UUIDField(
        unique=True, 
        db_index=True, 
        editable=False
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return self.username or str(self.profile_id)


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4,  editable=False)
    user = models.ForeignKey(Profile, default=uuid.uuid4, on_delete=models.CASCADE)
    title = models.TextField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f"{self.user_id} - {self.title}"

