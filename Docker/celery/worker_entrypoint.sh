#!/bin/zsh
celery -A webhook_service worker -l info
