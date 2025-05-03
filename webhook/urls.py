from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, IngestWebhookAPIView, EventStatusAPIView, SubscriptionAttemptsAPIView

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('ingest/<uuid:subscription_id>/', IngestWebhookAPIView.as_view(), name='ingest-webhook'),
    path('events/<uuid:event_id>/status/', EventStatusAPIView.as_view(), name='event-status'),
    path('subscriptions/<uuid:subscription_id>/attempts/', SubscriptionAttemptsAPIView.as_view(), name='subscription-attempts'),
]