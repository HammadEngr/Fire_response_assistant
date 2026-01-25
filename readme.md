# Fire Crisis Assistant Chatbot

_A Dockerized Fire Response & Education Assistant_

This project is a **production-style chatbot system** built using **Django**, **Rasa**, **Postgresql** and **Docker**, and deployed on **AWS EC2** behind **NGINX + Gunicorn**.

The goal of the project is to demonstrate:

- chatbot architecture
- backend–ML integration
- containerized deployment
- real-world DevOps workflow

---

## High-Level Architecture

```
Browser
   ↓
NGINX (Reverse Proxy)
   ↓
Gunicorn
   ↓
Django (API + UI)
   ↓
Rasa (NLU & Dialogue)
   ↓
Rasa Actions (Custom Logic)
```

All services run as **Docker containers**.

---

## Architecture Overview

```
Django Container
   - Admin Panel
   - Models
   - Migrations
   - View Layer

PostgreSQL Container
   - fire_categories
   - sub_categories
   - risk_levels
   - fire_responses
   - default_response
   - user_submissions

Rasa Container
Custom Actions
```

## Tech Stack

- Python 3.8
- Django 4.x
- Rasa 3.1.0
- Rasa SDK 3.1.0
- Postgresql
- Docker & Docker Compose
- NGINX
- Gunicorn
- AWS EC2 (Elastic IP)

---

## Project Structure

```
crisis_assistant/
├── docker-compose.prod.yml     # Production configuration
├── docker-compose.dev.yml      # Development overrides
├── docker-compose.yml          # Development overrides
├── django/                     # Django backend + UI
├── rasa/                       # Rasa NLU, rules, domain
├── actions/                    # Rasa custom actions
├── nginx/                      # NGINX config
├── .env.dev                    # Development environment
├── .env.prod                   # Production environment
└── README.md
```

---

## How to Run Locally (For Evaluation)

### Prerequisites

- Docker
- Docker Compose
- Git

No Python, virtualenv, or manual installs are required.

---

### Step 1: Clone the repository

```bash
git clone https://github.com/HammadEngr/Fire_response_assistant.git
cd crisis_assistant
```

---

### Step 2: Start the application (development mode)

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

This will:

- start Django using `runserver`
- start Rasa with API enabled
- enable live code reload
- expose the app on port **8000**

---

### Step 3: Train the chatbot model (one time)

```bash
docker exec -it rasa_server rasa train
```

---

### Step 4: Access the application

Open a browser and visit:

```
http://localhost:8000/
```

You can now interact with the chatbot UI.

---

## Production Deployment (AWS EC2)

The application is deployed on **AWS EC2** using:

- Docker Compose
- NGINX
- Gunicorn
- Elastic IP (static public access)

Once deployed, it is accessible from anywhere via:

```
http://<elastic-ip>/
```

No local machine is required to keep it running.

---

## Development → Deployment Workflow

1. Develop locally using `docker-compose.yml`
2. Commit and push changes
3. Pull on EC2
4. Deploy with:

   ```bash
   docker compose build
   docker compose up -d
   ```

---

## Key Engineering Decisions

- **Docker volumes** are used for:
  - Postgresql database persistence
  - Rasa trained models

- **No live reload in production** (safe deployment)
- **CSRF disabled only for API endpoints**
- **Elastic IP** used to avoid changing host configuration

---

## Notes for Evaluators

- The project demonstrates **real-world backend + ML integration**
- Uses **production deployment patterns**, not toy scripts
- Focuses on **correct system design**, not shortcuts
- The chatbot logic is intentionally **rule-driven** due to safety-critical nature (fire response)

---

## Current Status

- ✔ Fully dockerized
- ✔ Locally runnable in one command
- ✔ Deployed on AWS EC2
- ✔ Stable and accessible
- ✔ Ready for evaluation

---

## For Django-Html - IMPORTANT

This is important for Django-Html to work, without these lines templates will not work.

- make a settings.json file in django/.vscode and put these lines there.
  {
  "files.associations": {
  "**/\*.html": "html",
  "**/templates/**/\*.html": "django-html",
  "**/templates/**/\*": "django-txt",
  "**/requirements.{txt,in}": "pip-requirements",
  "\*_/requirements/_.{txt,in}": "pip-requirements"
  },
  "emmet.includeLanguages": {
  "django-html": "html"
  },
  "python-envs.defaultEnvManager": "ms-python.python:system",
  "python-envs.pythonProjects": []
  }

- make .prettierignore if using prettier as formater and put thi line there.
  **/templates/**/\*.html

## Contact

For any questions regarding setup or architecture, please contact the project author.

---

**End of README**
