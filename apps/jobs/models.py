from django.db import models
from apps.core.models import Profile
import uuid

class Job(models.Model):
    # Enums for Job Status
    class JobStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CLOSED = "closed", "Closed"

    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.TextField()
    company_info = models.TextField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    status = models.TextField(
        choices=JobStatus.choices, 
        default=JobStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "jobs"

    def __str__(self):
        return self.title
class Application(models.Model):
    # Enums for Application Status
    class ApplicationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    phone = models.TextField(null=True, blank=True)
    expected_salary = models.FloatField(null=True, blank=True)
    cv_url = models.TextField(null=True, blank=True)
    status = models.TextField(
        choices=ApplicationStatus.choices, 
        default=ApplicationStatus.PENDING
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "applications"

    def __str__(self):
        # Changed self.applicant_id to self.applicant.profile (or your Profile PK name)
        return f"{self.applicant} - {self.job.title}"