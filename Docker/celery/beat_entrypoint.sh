#!/bin/zsh
exec celery -A webhook_service beat -l info