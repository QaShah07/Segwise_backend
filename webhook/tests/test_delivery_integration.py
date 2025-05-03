import pytest, responses
from webhook.tasks import deliver_webhook
from webhook.models import Subscription, WebhookEvent, DeliveryAttempt

@pytest.mark.django_db
def test_delivery_and_retry(monkeypatch):
    sub = Subscription.objects.create(target_url='http://mock.test', event_types=[])
    event = WebhookEvent.objects.create(subscription=sub, payload={'a':1})

    # first call: simulate 500 error
    responses.add(responses.POST, sub.target_url, status=500)
    # second call: simulate success
    responses.add(responses.POST, sub.target_url, status=200)

    # run task synchronously
    deliver_webhook(event.id)

    attempts = DeliveryAttempt.objects.filter(webhook_event=event).order_by('attempt_number')
    assert attempts.count() == 2
    assert attempts[0].http_status == 500
    assert attempts[1].http_status == 200
    event.refresh_from_db()
    assert event.status == 'delivered'