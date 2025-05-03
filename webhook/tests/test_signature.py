import hmac, hashlib
from rest_framework.test import APIClient
import pytest
from webhook.models import Subscription

@pytest.mark.django_db
def test_invalid_signature_rejected():
    sub = Subscription.objects.create(target_url='http://ex.com', secret='s3cr3t', event_types=[])
    client = APIClient()
    payload = b'{"foo":1}'
    sig = 'sha256=' + hmac.new(b'wrong', payload, hashlib.sha256).hexdigest()
    resp = client.post(f'/api/ingest/{sub.id}/', payload, content_type='application/json', HTTP_X_HUB_SIGNATURE_256=sig)
    assert resp.status_code == 403