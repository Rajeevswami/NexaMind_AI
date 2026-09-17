import logging
from anthropic import AsyncAnthropic
from app.core.config import settings

logger = logging.getLogger(__name__)

async def get_completion(system_prompt: str, messages: list[dict], max_tokens: int = 1024, temperature: float = 0.4) -> str:
    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured")
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    try:
        response = await client.messages.create(model=settings.claude_model, max_tokens=max_tokens, temperature=temperature, system=system_prompt, messages=messages)
        return "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
    except Exception:
        logger.exception("Claude API call failed")
        raise

