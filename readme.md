# Crisis Assistant Chatbot

A Dockerized production ready **Fire Response Assistant** chatbot system built using Rasa, Django, and an external Action Server. The project demonstrates end-to-end chatbot architecture, API integration, and containerized deployment.

## Tech Stack

- Python: 3.8
- Rasa: 3.1.0
- Django: 4.2
- rasa sdk: 3.1.0
- Docker & Docker Compose
- postman (for api testing)

## Architecture

Browser → Django → Rasa → Action Server

## Responsibilites

- Django - API Layer, request handling
- Rasa - NLU + dialogue management
- Action server - custom business logic
- Docker - environment consistency

## Project Structure

crisis_assistant/
├── docker-compose.yml
├── rasa/
│ ├── data/
│ │ ├── nlu.yml
│ │ └── rules.yml
│ ├── domain.yml
│ ├── config.yml
│ ├── endpoints.yml
│ └── models/ # generated (ignored in git)
├── actions/
│ └── actions.py
├── django/
│ ├── manage.py
│ ├── config/
│ └── bot/
├── .gitignore
└── README.md

## How to Run Locally

### Prerequisites

- Docker installed and running
- Git installed

### Steps To Follow

- **step 1:** start containers (run this in new cli)
  docker compose up -d
- **step 2:** start action server (run this in new cli)
  docker exec -it action_server sh
  pip install websockets==10.4 sanic==21.12.0 rasa-sdk==3.1.0
  python -m rasa_sdk --actions actions --port 5055

  you should see:
  Registered actions: - action_hello_world

- **step 3:** tarin and start rasa (run this in new cli )
  docker exec -it rasa_server sh
  rasa train
  rasa run --enable-api --cors "\*"

- **step 4:** start django (run this in new cli)
  docker exec -it rasa_server sh
  rasa train --force
  rasa run --enable-api --cors "\*"

- **step 4:** test via django
  in post man send a POST request at http://localhost:8000/api/chat/ with body like this {
  "sender": "test",
  "message": "hello"
  }
  you should get a response like this [
  {
  "recipient_id": "test",
  "text": "Hello from action server!"
  }
  ]

- **Step 5:** test via Rasa directly at http://localhost:5005/webhooks/rest/webhook
  with same body send POST request at above url.
  you will get the same response as above

## Other auxiliary notes

## Notes

- Models are not committed; they are generated locally.
- External action server is used.

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
