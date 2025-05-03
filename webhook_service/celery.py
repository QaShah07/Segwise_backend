import os
from celery import Celery

env = os.getenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webhook_service.settings')
app = Celery('webhook_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Define periodic cleanup schedule
app.conf.beat_schedule = {
    'cleanup-old-attempts-every-hour': {
        'task': 'webhook.tasks.cleanup_delivery_attempts',
        'schedule': 3600,  # every hour
    },
}