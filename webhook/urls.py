from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, IngestWebhookAPIView

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('ingest/<uuid:subscription_id>/', IngestWebhookAPIView.as_view(), name='ingest-webhook'),
]