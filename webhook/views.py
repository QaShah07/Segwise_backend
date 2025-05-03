import hmac
import hashlib
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import Subscription, WebhookEvent
from .serializers import SubscriptionSerializer, WebhookEventSerializer
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

        # Create WebhookEvent
        event = WebhookEvent.objects.create(subscription=sub, payload=request.data)

        # Enqueue Celery task for async delivery
        deliver_webhook.delay(str(event.id))

        return Response({'event_id': event.id}, status=status.HTTP_202_ACCEPTED)