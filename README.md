#Project Structure
```bash
webhook_service/
│
├── app/
│   ├── webhook/              # Django app
│   ├── webhook_service/      # Django project
│   ├── manage.py
│   └── requirements.txt
│
├── docker/
│   ├── celery/
│   │   └── worker_entrypoint.sh
│   └── django/
│       └── entrypoint.sh
│
├── docker-compose.yml
├── Dockerfile
└── .env
```
# Database Connection Setup

## 1. Create a `.env` File
In the root of your project, create a `.env` file to store your MySQL database credentials:
```
DB_NAME=segwise
DB_USER=root
DB_PASSWORD=YourPasswordHere
DB_HOST=127.0.0.1
DB_PORT=3306
```
## 2. Update settings.py in Your Django Project
In your settings.py, import the config function from decouple at the top:
```
from decouple import config
```
Then update the DATABASES configuration to use the .env variables:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

#Project Structure
```bash
webhook_service/
│
├── app/
│   ├── webhook/              # Django app
│   ├── webhook_service/      # Django project
│   ├── manage.py
│   └── requirements.txt
│
├── docker/
│   ├── celery/
│   │   └── worker_entrypoint.sh
│   └── django/
│       └── entrypoint.sh
│
├── docker-compose.yml
├── Dockerfile
└── .env
```