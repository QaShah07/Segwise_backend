import hmac
import hashlib
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Subscription, WebhookEvent, DeliveryAttempt
from .serializers import SubscriptionSerializer, WebhookEventSerializer, DeliveryAttemptSerializer
from .tasks import deliver_webhook

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all().order_by('-created_at')
    serializer_class = SubscriptionSerializer

class IngestWebhookAPIView(APIView):
    """
    POST /ingest/{subscription_id}/  → 202 Accepted + enqueue
    """
    def post(self, request, subscription_id):
        sub = get_object_or_404(Subscription, id=subscription_id)

        # Optional signature verification
        if sub.secret:
            signature = request.headers.get('X-Hub-Signature-256')
            if not signature:
                return Response({'detail': 'Missing signature header.'}, status=status.HTTP_400_BAD_REQUEST)
            body = request.body
            computed = 'sha256=' + hmac.new(sub.secret.encode(), body, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(computed, signature):
                return Response({'detail': 'Invalid signature.'}, status=status.HTTP_403_FORBIDDEN)

        event = WebhookEvent.objects.create(subscription=sub, payload=request.data)
        deliver_webhook.delay(str(event.id))
        return Response({'event_id': event.id}, status=status.HTTP_202_ACCEPTED)

class EventStatusAPIView(APIView):
    """
    GET /events/{event_id}/status/ → return event + last N attempts
    """
    def get(self, request, event_id):
        event = get_object_or_404(WebhookEvent, id=event_id)
        # number of attempts to return
        limit = int(request.query_params.get('limit', 10))
        attempts = event.attempts.order_by('-attempted_at')[:limit]
        event_data = WebhookEventSerializer(event).data
        attempts_data = DeliveryAttemptSerializer(attempts, many=True).data
        return Response({'event': event_data, 'attempts': attempts_data}, status=status.HTTP_200_OK)

class SubscriptionAttemptsAPIView(APIView):
    """
    GET /subscriptions/{subscription_id}/attempts/?limit=20&page=1
    """
    def get(self, request, subscription_id):
        sub = get_object_or_404(Subscription, id=subscription_id)
        limit = int(request.query_params.get('limit', 20))
        page = int(request.query_params.get('page', 1))
        # gather attempts across all events for this subscription
        qs = DeliveryAttempt.objects.filter(webhook_event__subscription=sub).order_by('-attempted_at')
        start = (page - 1) * limit
        end = start + limit
        items = qs[start:end]
        data = DeliveryAttemptSerializer(items, many=True).data
        total = qs.count()
        return Response({
            'subscription_id': str(sub.id),
            'page': page,
            'limit': limit,
            'total_attempts': total,
            'attempts': data
        }, status=status.HTTP_200_OK)