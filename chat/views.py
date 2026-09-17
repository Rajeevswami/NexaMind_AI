import json
import logging
import re

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .models import ChatMessage, ChatSession

logger = logging.getLogger(__name__)
HISTORY_LIMIT = 15

@login_required
def index(request):
    sessions = ChatSession.objects.filter(owner=request.user)
    active = sessions.first()
    return render(request, "chat/index.html", {"sessions": sessions, "active_session": active})

def _title_for(message: str) -> str:
    words = re.findall(r"\S+", message)
    return " ".join(words[:6])[:255] or "New conversation"

@login_required
@require_GET
def session_list(request):
    sessions = ChatSession.objects.filter(owner=request.user).values("id", "title", "updated_at")
    return JsonResponse({"sessions": list(sessions)})

@login_required
@require_POST
def create_session(request):
    session = ChatSession.objects.create(owner=request.user)
    return JsonResponse({"id": session.id, "title": session.title, "updated_at": session.updated_at.isoformat()}, status=201)

@login_required
@require_GET
def session_detail(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, owner=request.user)
    messages = session.messages.order_by("created_at").values("id", "role", "content", "created_at")
    return JsonResponse({"id": session.id, "title": session.title, "messages": list(messages)})

@login_required
@require_POST
def send_message(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, owner=request.user)
    try:
        payload = json.loads(request.body)
        question = str(payload.get("message", "")).strip()
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid request body."}, status=400)
    if not question:
        return JsonResponse({"error": "A message is required."}, status=400)
    if len(question) > 20_000:
        return JsonResponse({"error": "Message is too long."}, status=400)
    history = list(session.messages.order_by("created_at").values("role", "content")[:HISTORY_LIMIT])
    try:
        response = requests.post(f"{settings.AI_SERVICE_URL}/ai/chat", json={"user_id": request.user.id, "question": question, "history": history}, headers={"X-Internal-Api-Key": settings.INTERNAL_API_KEY}, timeout=settings.AI_SERVICE_TIMEOUT)
        response.raise_for_status()
        answer = response.json()["answer"]
    except (requests.RequestException, KeyError, ValueError):
        logger.exception("AI service request failed for user_id=%s", request.user.id)
        return JsonResponse({"error": "AI service is unavailable right now. Please try again."}, status=502)
    with transaction.atomic():
        if not session.messages.exists() and session.title == "New conversation":
            session.title = _title_for(question)
        ChatMessage.objects.create(session=session, role=ChatMessage.Role.USER, content=question)
        ChatMessage.objects.create(session=session, role=ChatMessage.Role.ASSISTANT, content=answer)
        session.save()
    return JsonResponse({"answer": answer, "title": session.title})
