from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.core.cache import cache
import requests
from .models import WebhookEvent, DeliveryAttempt

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=5)
def deliver_webhook(self, event_id):
    """
    Deliver payload to target_url, record attempts, retry with backoff.
    """
    try:
        event = WebhookEvent.objects.select_related('subscription').get(id=event_id)
        sub = event.subscription
        # fetch subscription from cache if available
        # cache key pattern: subscription:{id}
        cached = cache.get(f'subscription:{sub.id}')
        if cached:
            sub = cached
        else:
            cache.set(f'subscription:{sub.id}', sub, timeout=300)

        resp = requests.post(sub.target_url, json=event.payload, timeout=10)
        DeliveryAttempt.objects.create(
            webhook_event=event,
            attempt_number=self.request.retries + 1,
            http_status=resp.status_code,
            error_text=None
        )
        if 200 <= resp.status_code < 300:
            event.status = 'delivered'
            event.save()
        else:
            raise Exception(f'HTTP {resp.status_code}')

    except Exception as exc:
        # record failed attempt
        DeliveryAttempt.objects.create(
            webhook_event_id=event_id,
            attempt_number=self.request.retries + 1,
            http_status=getattr(exc, 'response', None) and exc.response.status_code,
            error_text=str(exc)
        )
        # if max retries reached, mark event failed
        if self.request.retries >= self.max_retries:
            WebhookEvent.objects.filter(id=event_id).update(status='failed')
            logger.error(f"Event {event_id} failed after max retries.")
            return
        # exponential backoff schedule
        backoff = [10, 30, 60, 300, 900]
        countdown = backoff[self.request.retries]
        raise self.retry(exc=exc, countdown=countdown)

@shared_task
def cleanup_delivery_attempts():
    """
    Delete DeliveryAttempt rows older than 72 hours.
    """
    cutoff = timezone.now() - timezone.timedelta(hours=72)
    deleted, _ = DeliveryAttempt.objects.filter(attempted_at__lt=cutoff).delete()
    logger.info(f"Cleaned up {deleted} old delivery attempts.")