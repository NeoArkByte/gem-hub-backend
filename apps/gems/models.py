from django.db import models
from apps.core.models import Profile
import uuid

class GemListing(models.Model):
    # Enums for Gem Status
    class GemStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    gem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Removed default=uuid.uuid4 from owner to ensure data integrity
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField()
    carat = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    variety = models.TextField(null=True, blank=True, default="Variety")
    color = models.TextField(null=True, blank=True, default="Blue")
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    seller_phone = models.TextField(null=True, blank=True)
    certificate_url = models.TextField(null=True, blank=True, default=" https://www.orimi.com/pdf-test.pdf")
    status = models.TextField(
        choices=GemStatus.choices,
        default=GemStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "gem_listings"

    def __str__(self):
        return self.name