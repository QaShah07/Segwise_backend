#!/bin/zsh
# Wait for DB/Redis to be ready
# (optional: add wait-for-it script)

# Start Celery worker
exec celery -A webhook_service worker -l info
```  

