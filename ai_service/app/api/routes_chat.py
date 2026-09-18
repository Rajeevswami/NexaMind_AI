import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.core.security import verify_internal_key
from app.core.config import settings
from app.core.rate_limit import limiter
from app.llm.client import get_completion
from app.llm.prompts import build_chat_system_prompt
from app.rag.pipeline import build_context
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["chat"], dependencies=[Depends(verify_internal_key)])

@router.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    context, sources = build_context(payload.question, payload.user_id, payload.document_id)
    messages = [{"role": message.role, "content": message.content} for message in payload.history[-15:]]
    messages.append({"role": "user", "content": payload.question})
    try:
        answer = await get_completion(build_chat_system_prompt(context or None), messages)
    except RuntimeError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI service is not configured") from error
    logger.info("Completed chat request user_id=%s history_turns=%s", payload.user_id, len(payload.history))
    return ChatResponse(answer=answer, sources=[{"document_id": source["document_id"], "page_number": source["page_number"]} for source in sources])
