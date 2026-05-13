from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "job_id",
        "title",
        "employer_id",
        "salary",
        "status",
        "created_at",
    )
    search_fields = ("title", "employer_id", "salary", "status")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "application_id",
        "job",
        "applicant_id",
        "phone",
        "expected_salary",
        "status",
        "applied_at",
    )
    search_fields = ("applicant_id", "phone", "expected_salary", "status")
    list_filter = ("status", "applied_at")
    ordering = ("-applied_at",)
    readonly_fields = ("applied_at",)
