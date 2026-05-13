from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from drf_api_logger.models import APILogsModel

@shared_task
def cleanup_api_logs(days_to_keep=7):
    """
    Deletes API logs older than the specified number of days.
    Default is 7 days to keep your database lean.
    """
    threshold_date = timezone.now() - timedelta(days=days_to_keep)
    deleted_count, _ = APILogsModel.objects.filter(added_on__lt=threshold_date).delete()
    return f"Deleted {deleted_count} old API logs."