# Debugging Notes: Django + Rasa + Docker (AWS EC2)

This document is the record of real debugging issues which i faced with their root cause and solutions while deploying a Django + Rasa application using Docker on AWS EC2. and i created it for my own record.

The goal is to:

    - avoid repeating the same mistakes
    - understand why fixes work
    - build independent debugging skills

# Project Structure (Final & Correct)

crises_response_app/
├── docker-compose.yml
├── .env
│
├── django/
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── manage.py
│ ├── project/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ │ └── asgi.py
│ └── chat_api/
│
├── rasa/
│ ├── config.yml
│ ├── domain.yml
│ ├── data/
│ └── models/
│
└── actions/

### Important rule: docker-compose.yml and .env always live at the project root.

# Problem 1: Django project had config/config nesting

Symptoms

    - ModuleNotFoundError: No module named config.settings

    - Gunicorn failing to boot

    - Confusing import paths

Root Cause - The Django project was created inside an already-named folder, resulting in:

This breaks:

    - Gunicorn imports
    - Django settings resolution

Solution: Recreate Django cleanly:

# Problem 2: Gunicorn could not find WSGI module

ModuleNotFoundError: No module named 'config.wsgi'

Root Cause

    - Gunicorn was pointed to the wrong import path.

Solution

    - Always match Gunicorn to the Django project package:
    CMD gunicorn project.wsgi:application --bind 0.0.0.0:8000

# Problem 3: Rasa training failed with permission error

Error: PermissionError: [Errno 13] Permission denied: 'config.yml'

Root Cause:

    Rasa container tried to write to config.yml
    File was bind mount from host
    Host file owned by ubuntu
    Container runs as a different UID
    Linux permissions are enforced by UID, not username

Key Diagnostic Commands Used
docker compose config # Truth source for mounts
docker compose exec rasa id # Shows container UID/GID
ls -l rasa/config.yml # Shows file ownership
docker compose exec rasa ls -l /app

Attempted Fixes That Did NOT Work
Attempt Why it failed
chmod 777 Insecure, bad practice
Adding assistant_id only Rasa still attempts file write
chown Host filesystem prevented ownership change
Running as root Anti-pattern

Correct & Final Solution

Run the Rasa container as the same user that owns the files on the host.

Step 1: Add user mapping to docker-compose.yml
rasa:
image: rasa/rasa:3.6.20
container_name: rasa_service
user: "${UID}:${GID}"
volumes: - ./rasa:/app
ports: - "5005:5005"
command: - run - --enable-api - --cors - "\*" - --debug

Step 2: Export UID/GID on host
export UID=$(id -u)
export GID=$(id -g)

Step 3: Restart services
docker compose down
docker compose up --build

Step 4: Train Rasa
docker compose exec rasa rasa train

# Key Lessons Learned

1️. Docker cares about UID, not usernames

    ubuntu ≠ UID 1000 inside container

    Bind mounts preserve host ownership

2. Always verify assumptions

Use:

    docker compose config
    docker exec <container> id
    ls -l

3. Don’t fight the filesystem

If ownership cannot be changed:

adapt container user instead

4. Debug layer by layer
   Code → Framework → Runtime → Container → OS → Cloud
   Only one layer is broken at a time.
