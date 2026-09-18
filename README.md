# NexaMind AI

> A full-stack AI knowledge and career assistant for document-aware chat, resume feedback, and personalized study plans.

NexaMind pairs a Django web app with an isolated FastAPI AI service. Users can upload documents, manage conversations, and access career tools while document retrieval remains scoped to the authenticated user.

## Features

- Secure Django authentication and private document uploads
- ChatGPT-inspired chat UI: history, new chat, retry, copy, responsive sidebar, and theme preference
- Anthropic Claude chat with bounded conversation memory
- RAG pipeline: PDF/DOCX/TXT extraction → chunking → embeddings → Qdrant retrieval
- Resume analysis, study-plan generation, and career-advice APIs
- Internal Django ↔ FastAPI API-key authentication
- Docker, PostgreSQL, Redis, Qdrant, and Nginx deployment configuration

## Architecture

```text
Browser → Django (auth, templates, uploads) → FastAPI (Claude, RAG, agents)
               │                                  │
        SQLite / PostgreSQL                 Qdrant vectors
```

The browser never receives Anthropic credentials or the internal service key.

## Stack

| Layer | Technology |
| --- | --- |
| Web | Django Templates, Tailwind CSS, Alpine.js |
| AI | FastAPI, Anthropic Claude |
| Retrieval | Sentence Transformers, Qdrant, PyMuPDF, python-docx |
| Infrastructure | Docker Compose, Redis, Nginx |

## Run Locally

Install dependencies:

```powershell
pip install -r requirements.txt
pip install -r ai_service\requirements.txt
```

Create root `.env`:

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-value
DJANGO_DEBUG=True
AI_SERVICE_URL=http://127.0.0.1:8001
INTERNAL_API_KEY=one-long-random-secret
```

Create `ai_service/.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
INTERNAL_API_KEY=use-the-same-secret-as-root-env
QDRANT_URL=http://127.0.0.1:6333
REDIS_URL=redis://localhost:6379/0
```

Run each service in a separate terminal:

```powershell
python manage.py migrate
python manage.py runserver
```

```powershell
cd ai_service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

```powershell
docker run --name nexamind-qdrant -p 6333:6333 qdrant/qdrant
```

Open [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/). Use HTTP, not HTTPS, with Django's development server.

## Verification

```powershell
python manage.py check
python manage.py test
Invoke-WebRequest http://127.0.0.1:8001/health
```

## Internal AI API

All `/ai/*` endpoints require `X-Internal-Api-Key`.

| Endpoint | Purpose |
| --- | --- |
| `POST /ai/chat` | Chat with optional document context |
| `POST /ai/documents/process` | Extract and index a document |
| `POST /ai/documents/search` | Inspect retrieval results |
| `POST /ai/resume/analyze` | Structured resume feedback |
| `POST /ai/study-plan/generate` | Study-plan generation |
| `POST /ai/career/advice` | Career guidance |
| `GET /health` | Service health check |

## Security

- Django document/chat queries are owner-scoped.
- Qdrant retrieval always filters by `user_id` and carries `document_id` metadata.
- Secrets live in `.env` files and must never be committed.
- Upload type and size are validated.

## Roadmap

- Celery-based automatic document processing
- Streaming answers and rendered source citations
- Usage limits, subscriptions, and monitoring

## License

For learning and portfolio use.
