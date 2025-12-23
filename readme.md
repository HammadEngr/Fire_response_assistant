## PHASE 0

### Fixed tech stack

    Python 3.8
    Rasa 3.1.0
    Django 4.2
    Docker + Docker Compose
    VS Code

## PHASE 1

### Fixed architecture (very important)

    1. Client (browser)
    2. Django (later)
    3. Rasa Server
    4. External Action Server

### Folder Structure

    docker-compose.yml
    rasa/
    actions/
    django/

## PHASE 2

### 2.1 Docker-compose.yml

    Services:
        rasa_server → Rasa runtime
        rasa_actions → External action server
        django_web → Placeholder for Django

    All containers:
        Python 3.8
        Volume mounted
        Ports exposed

### 2.2 Learned critical Docker concept

    Official Rasa image has an ENTRYPOINT
    command: tail -f /dev/null alone does NOT work

## PHASE 3

### 3.1 Entered Rasa container

    docker exec -it rasa_server sh
    rasa init --no-prompt
    rasa run --enable-api --cors "*"
    http://localhost:5005/status

## PHASE 4 — External Action Server Setup

### 4.1 Entered action server container

    docker exec -it rasa_actions sh
    pip install rasa-sdk==3.1.0

    pip uninstall -y websockets sanic
    pip install sanic==21.12.0 websockets==10.4

    python -m rasa_sdk --port 5055

## CURRENT STATUS (important)

    You now have:

    ✅ Dockerized Rasa 3.1.0
    ✅ External Action Server
    ✅ Correct dependency pinning
    ✅ Clean rule-based logic
    ✅ Stable, production-style architecture

    🚫 No Django yet (intentionally)
