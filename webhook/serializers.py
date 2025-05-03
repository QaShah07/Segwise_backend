from rest_framework import serializers
from .models import Subscription, WebhookEvent, DeliveryAttempt

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'target_url', 'secret', 'event_types', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_target_url(self, value):
        # DRF URLField already validates URL format
        return value

    def validate_event_types(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("event_types must be a list of strings.")
        for evt in value:
            if not isinstance(evt, str):
                raise serializers.ValidationError("each event type must be a string.")
        return value

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ['id', 'subscription', 'payload', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

class DeliveryAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAttempt
        fields = ['id', 'webhook_event', 'attempt_number', 'http_status', 'error_text', 'attempted_at']
        read_only_fields = ['id', 'attempted_at']