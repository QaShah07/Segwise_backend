import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField  # Django≥3.1 use models.JSONField

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_url = models.URLField()
    secret = models.CharField(max_length=255, blank=True, null=True)
    # store as JSON array of strings; MySQL 5.7+ supports JSON
    event_types = models.JSONField(default=list, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription {self.id} → {self.target_url}"


class WebhookEvent(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name='events'
    )
    payload = models.JSONField()   # JSON payload
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id} ({self.status})"


class DeliveryAttempt(models.Model):
    webhook_event = models.ForeignKey(
        WebhookEvent, on_delete=models.CASCADE, related_name='attempts'
    )
    attempt_number = models.PositiveSmallIntegerField()
    http_status = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['attempted_at']),
            models.Index(fields=['webhook_event', 'attempt_number']),
        ]

    def __str__(self):
        return f"Attempt #{self.attempt_number} for {self.webhook_event.id}"
