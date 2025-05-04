# Webhook Delivery System Assignment

A Django-based webhook management platform with subscription support, async delivery via Celery, retry/backoff logic, Redis caching, and a minimal React dashboard. Easily test, monitor, and scale webhook events across client targets.

##  Deployment

The application is deployed and accessible at: [Live Demo](https://segwise-backend-4.onrender.com)

You can use the live link to test the frontend and backend without local setup.

##  Tech Stack
- **Backend:** Django, celery, Redish
- **Frontend:** ReactJS, react axios
- **Containerization:** Docker, Docker Compose

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
## Important Note:
- To **run locally with Docker**, simply remove the comment on the Docker-related lines in the configuration file and comment out the lines for **Render deployment**.
- For **Render deployment**, comment out the Docker-related lines and uncomment the lines for Renders.

##  Clone Instructions

To clone this repository to your local machine, follow these steps:

1. Open your terminal
2. Run the following command:

```bash
 git clone https://github.com/QaShah07/Segwise_backend.git
 ```
3. Navigate to the project directory:
 ```
 cd Segwise_backend
 ```
## Option 1️⃣: Docker Setup
###  Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed
### Run the app
From the root project directory:
```bash
docker-compose build --no-cache
docker-compose up

```
### To stop the containers:
```
docker-compose down
```

## Option 2️⃣: Manual Setup

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
DJANGO_SECRET_KEY=your-secret
# Database Connection Manual
# DB_NAME=segwise
# DB_USER=root
# DB_PASSWORD=your password
# DB_HOST=127.0.0.1
# DB_PORT=3306
# Database connection for Docker
DB_NAME=webhook_db
DB_USER=webhook_user      # must not be 'root'
DB_PASSWORD=webhook_pass
DB_HOST=db
DB_PORT=3306
#Redis server connection
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
        'HOST': config('DB_HOST', default='db'),  # service name in docker-compose network
        'PORT': config('DB_PORT', default='3306'),
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
## 2️⃣ Frontend (ReactJS) ~ Optional 
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
npm run dev
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
## Verify

   * Django API: [http://localhost:8000/api/](http://localhost:8000/api/)
   * Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)


##  Architecture Overview

This service is designed for reliability, scalability, and ease of development:

* **Framework (Django + DRF):** Django offers rapid API scaffolding, built‑in security, and an extensible ORM. DRF adds powerful serialization, viewsets, and browsable API documentation.
* **Database (MySQL):** A robust relational store with native JSON field support for flexible payload storage. We chose MySQL for its reliability, horizontal scalability, and free-tier availability on cloud platforms.
* **Cache & Broker (Redis):** Redis serves dual purposes: caching frequent subscription lookups to reduce DB load and acting as Celery’s message broker for high-throughput task queuing.
* **Async Task Queue (Celery):** Enables asynchronous delivery of webhooks, decoupling ingestion from delivery. Celery’s built‑in retry mechanisms and pluggable backends provide resilience under failure.
* **Retry Strategy:** Exponential backoff with intervals \[10s, 30s, 1m, 5m, 15m], capped at 5 attempts. This balances prompt delivery against upstream receiver availability and rate-limits.
* **Containerization (Docker Compose):** Ensures a consistent environment across development, testing, and production. Leveraging Docker Compose accelerates local onboarding and CI/CD pipelines.

| Component        | Technology          | Rationale                                         |
| ---------------- | ------------------- | ------------------------------------------------- |
| API Framework    | Django + DRF        | Rapid development, built-in admin, authentication |
| Database         | MySQL               | JSONField support, reliability                    |
| Cache & Broker   | Redis               | Fast caching & Celery broker                      |
| Task Queue       | Celery              | Reliable background processing, retries           |
| Frontend         | React + React Query | Declarative UI, caching and async data            |
| Containerization | Docker Compose      | Consistent local/dev and CI environments          |

##  Database Schema & Indexing

Our schema is optimized for write-heavy ingestion and read-heavy status queries:

1. **Subscription Table:**

   * **UUID PK** for globally unique identifiers.
   * **JSON field** for `event_types` allows flexible subscription filters without schema migrations.
   * **Timestamps** (`created_at`, `updated_at`) support audit and TTL cleanup in future.

2. **WebhookEvent Table:**

   * **JSON payload** stores arbitrary webhook bodies.
   * **ENUM status** with an index for fast querying of pending or failed events in dashboards or retries.
   * **Index on `created_at`** to efficiently paginate or prune old events.

3. **DeliveryAttempt Table:**

   * **Composite index** on `(webhook_event_id, attempt_number)` accelerates retrieval of the latest attempts per event.
   * **Index on `attempted_at`** enables scheduled cleanup of logs older than 72 hours.

Together, these indexes ensure quick lookups for API queries (e.g., status pages) while minimizing write contention during high-volume ingestion.

##  Cost Estimate (Monthly)

| Service           | Free Tier Limits           | Estimated Cost |
| ----------------- | -------------------------- | -------------- |
| Cloud SQL         | db-f1-micro instance       | \$0            |
| Memorystore Redis | 30 MB                      | \$0            |
| Cloud Run         | 180k vCPU-sec, 360k GB-sec | \$0            |
| Egress & Storage  | Low usage                  | \$0            |

**Total:** \~\$0 / month (within free tiers)


##  Assumptions

* Average payload < 1 MB
* 5,000 ingestions/day, 1.2 attempts each
* Single-region deployment (us-central1)


## Credits

* **StackOverflow & Official Docs:** Problem-solving and best-practice references.
* **ChatGPT (OpenAI):** Assisted in architecture planning, documentation drafting, and code examples.
* **Postman :** Used for API testing for the project.