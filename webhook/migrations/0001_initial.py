# Generated by Django 5.2 on 2025-05-03 05:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('target_url', models.URLField()),
                ('secret', models.CharField(blank=True, max_length=255, null=True)),
                ('event_types', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payload', models.JSONField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='webhook.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_number', models.PositiveSmallIntegerField()),
                ('http_status', models.IntegerField(blank=True, null=True)),
                ('error_text', models.TextField(blank=True, null=True)),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
                ('webhook_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='webhook.webhookevent')),
            ],
            options={
                'indexes': [models.Index(fields=['attempted_at'], name='webhook_del_attempt_d85478_idx'), models.Index(fields=['webhook_event', 'attempt_number'], name='webhook_del_webhook_d89414_idx')],
            },
        ),
    ]
