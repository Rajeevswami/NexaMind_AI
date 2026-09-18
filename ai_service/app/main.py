from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_chat, routes_documents, routes_health
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()
app = FastAPI(title="NexaMind AI Service", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_methods=["*"], allow_headers=["*"])
app.include_router(routes_health.router)
app.include_router(routes_chat.router)
app.include_router(routes_documents.router)
