# AI Chatbot (Django)

A minimal document-question chatbot built with Django and Django REST Framework.

## Features

- Register/login/logout flow
- Upload a document (`.txt`, `.md`, `.pdf`)
- Ask questions against uploaded content
- Clean web UI at `/app/` (after login)
- REST endpoints:
  - `POST /api/upload/`
  - `POST /api/chat/`

## Project Layout

- `config/` - Django settings and root URL config
- `apps/chatbot/` - chatbot API, services, models, tests
- `templates/chatbot/index.html` - frontend page
- `static/chatbot/` - CSS and JS assets

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations chatbot
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

The app entrypoint redirects anonymous users to `/register/`, then login at `/login/`.

## Run Tests

```bash
python manage.py test
```

# Ai_ChatBot
