import pytest
from webhook.models import Subscription, WebhookEvent, DeliveryAttempt
from django.utils import timezone
import uuid

pytestmark = pytest.mark.django_db

def test_subscription_creation():
    sub = Subscription.objects.create(
        target_url='https://example.com/webhook',
        secret='secret123',
        event_types=['order.created']
    )
    assert sub.id is not None
    assert sub.event_types == ['order.created']


def test_webhook_event_default_status():
    sub = Subscription.objects.create(target_url='https://ex.com', event_types=[])
    event = WebhookEvent.objects.create(subscription=sub, payload={'x':1})
    assert event.status == 'pending'
    assert event.created_at <= timezone.now()