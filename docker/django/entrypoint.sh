#!/bin/zsh
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files (if using)
# python manage.py collectstatic --noinput

# Start Django server
exec gunicorn webhook_service.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3