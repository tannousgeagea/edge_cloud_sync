from django.db import models

# Create your models here.
class Event(models.Model):

    PENDING = 'pending'
    PROCESSING = 'processing'
    FAILED = 'failed'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (FAILED, 'Failed'),
        (COMPLETED, 'Completed'),
    ]

    event_id = models.CharField(max_length=255, unique=True)
    source_id = models.CharField(max_length=255, null=True, blank=True, help_text="Source system or service that generated this event")
    data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        db_index=True,
    )
    retry_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "event"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['event_id']),
            models.Index(fields=['source_id']),
        ]

        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"Event {self.event_id} - Status: {self.status}"

class MediaFile(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media_files')  # Link to the related event
    file_path = models.CharField(max_length=512, help_text="File path or URL to the media file")
    retry_count = models.PositiveIntegerField(default=0)
    uploaded = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['uploaded', 'created_at']),
        ]
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Files'

    def __str__(self):
        return f"Media File for Event {self.event.event_id} - Uploaded: {self.uploaded}"