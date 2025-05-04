##  Tech Stack
- **Backend:** Django, celery, Redish
- **Frontend:** ReactJS, react axios
## Project Structure
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

## UI dashboard
```bash
dashboard/src/
├── api/
├── components/
├── pages/
└── App.tsx     
```
---
## 🖥️ Clone Instructions

To clone this repository to your local machine, follow these steps:

1. Open your terminal
2. Run the following command:

   ```bash
    git clone https://github.com/QaShah07/Segwise_backend.git
    ```
3. Navigate to the project directory:
```
cd webhook_service
```

## Option 1️⃣: Manual Setup

## 1️⃣ Backend (Django)
1. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate 
```

2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a .env file inside the backend directory with the following content:
```env
# Secret Key
DJANGO_SECRET_KEY=your_django_secret_key

# Database Connection
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Redis server connection
REDIS_URL=redis://redis:6379/0
```
4. Update settings.py in Your Django Project
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
5. Apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```

6. Run the server:
```
python manage.py runserver
```
## 2️⃣ Frontend (ReactJS)
1. Navigate to the frontend directory:
```
cd dashboard
```
2. Install dependencies:
```
npm install
```
3. Start the React development server:
```
npm start
```
## Option 2️⃣: Docker Setup
###  Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed
### Run the app
From the root project directory:
```bash
docker-compose up --build
```
### To stop the containers:
```
docker-compose down
```


##  API Endpoints
| Method | Endpoint                         | Description             |
|--------|---------------------------------|------------------------|
| POST   | /api/subscriptions/              | Create a subscription  |
| POST   | /api/ingest/<sub_id>/            | Ingest data            |
| GET    | /api/events/<event_id>/status/   | Get event status       |

##  API Usage (sample `curl`)

```bash
### Create subscription
curl -X POST http://localhost:8000/api/subscriptions/ \
     -H 'Content-Type:application/json' \
     -d '{"target_url":"http://...","event_types":["order.created"]}'
```
### Ingest
```
curl -X POST http://localhost:8000/api/ingest/<sub_id>/ \
     -H 'Content-Type:application/json' \
     -d '{"order_id":1}'
```

### Check status
```
curl http://localhost:8000/api/events/<event_id>/status/?limit=5
```

##  Deployment

The application is deployed and accessible at:

👉 [Live Demo](https://your-deployment-url.com)

You can use the live link to test the frontend and backend without local setup.
