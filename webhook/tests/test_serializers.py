import pytest
from webhook.serializers import SubscriptionSerializer

@pytest.mark.parametrize('data,valid', [
    ({'target_url':'http://a.com','event_types':['e']}, True),
    ({'target_url':'not-a-url','event_types':['e']}, False),
    ({'target_url':'http://a.com','event_types':'e'}, False),
])
def test_subscription_serializer(data, valid):
    serializer = SubscriptionSerializer(data=data)
    assert serializer.is_valid() is valid