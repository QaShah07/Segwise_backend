from celery import shared_task
from .models import WebhookEvent
from django.core.cache import cache
import requests

@shared_task(bind=True, max_retries=5)
def deliver_webhook(self, event_id):
    """
    Fetch the event, perform delivery to subscription.target_url,
    record DeliveryAttempt, retry on failure with exponential backoff.
    """
    try:
        event = WebhookEvent.objects.select_related('subscription').get(id=event_id)
        sub = event.subscription

        # Prepare payload & headers
        url = sub.target_url
        data = event.payload
        resp = requests.post(url, json=data, timeout=10)

        # TODO: record DeliveryAttempt here (Phase 3)
        if resp.status_code < 300:
            event.status = 'delivered'
            event.save()
        else:
            raise Exception(f"Bad status {resp.status_code}")
    except Exception as exc:
        # retry with backoff
        countdown = [10, 30, 60, 300, 900][self.request.retries]
        raise self.retry(exc=exc, countdown=countdown)