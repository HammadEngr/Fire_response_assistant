# Django + Rasa Deployment Notes (AWS EC2 + Docker)

This document records the **key learnings, problems faced, and correct solutions**
while deploying a Django + Rasa application on AWS EC2 using Docker, Gunicorn, and NGINX.

It is written for **future reference** so the same mistakes are not repeated.

---

## 1. High-level Architecture

Browser
↓
NGINX (port 80)
↓
Gunicorn
↓
Django (API + UI)
↓
Rasa (NLU)
↓
Rasa Actions

All services run as **Docker containers** on an **AWS EC2 instance**.

---

## 2. Local vs Production (Mental Model)

| Aspect        | Local Dev   | Production (EC2)        |
| ------------- | ----------- | ----------------------- |
| Server        | runserver   | Gunicorn                |
| Reverse Proxy | none        | NGINX                   |
| Debug         | True        | False                   |
| Reload        | live reload | rebuild/restart         |
| DB            | SQLite      | SQLite (volume-mounted) |
| Access        | localhost   | Elastic IP              |

Same codebase, **different runtime behavior**.

---

## 3. Docker Rules That Matter (VERY IMPORTANT)

### 3.1 Containers are ephemeral

- Anything **inside the container filesystem** is lost on rebuild.
- Persistent data must live in **Docker volumes**.

### 3.2 Code vs Data

| Item               | Should Persist? | How           |
| ------------------ | --------------- | ------------- |
| Django code        | ❌              | rebuild image |
| Static files       | ❌              | collectstatic |
| SQLite DB          | ✅              | volume        |
| Rasa models        | ✅              | bind mount    |
| Django sessions    | ✅              | DB            |
| ML training output | ✅              | volume        |

---

## 4. Django Configuration Lessons

### 4.1 ALLOWED_HOSTS (Production)

- EC2 public IP changes on restart → **bad**
- **Solution: Elastic IP**

```env
DJANGO_ALLOWED_HOSTS=<elastic-ip>

Never use
ALLOWED_HOSTS = ["*"]  # ❌ in production

```

### 4.2 SECRET_KEY

    - Must be set via environment variable
    - Never empty in production
    - DJANGO_SECRET_KEY=some-long-random-string

### 4.3 CSRF for APIs

API endpoints using fetch() are blocked by CSRF by default

Correct fix for APIs:

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_response(request):
...

## 5. SQLite + Docker (Major Pitfall)

Wrong

    - Mounting SQLite directly as a file:

        - db_volume:/app/db.sqlite3

Correct

    Mount a directory, not a file:

        settings.py

        DATABASES = {
        "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db" / "db.sqlite3",
        }
        }

        docker-compose.yml
            volumes:
                - db_volume:/app/db

## 6. Django Sessions Error (no such table: django_session)

Cause

    Migrations not applied to the actual runtime DB
    Or DB wiped due to rebuild without volume

Fix
docker exec -it django_web python manage.py migrate

## 7. Gunicorn vs print()

Problem

    print() does not show logs reliably under Gunicorn

Correct debugging

Use logging:

import logging
logger = logging.getLogger(**name**)

logger.error("DJANGO VIEW HIT")

## 8. Rasa-Specific Lessons

10.1 Rasa requires a trained model

If you see:

No valid model found at models! rasa will return []

### Rasa permission issues on EC2

Root cause: Rasa image runs as non-root

Host files owned by root

Practical fix (acceptable for demos):
rasa:
user: root
