from app.llm.client import get_completion
async def get_career_advice(question: str, target_role: str, resume_text: str | None = None) -> str:
    return await get_completion("You are NexaMind, a direct software-career advisor. Give specific practical next steps; use provided resume context only when present.", [{"role":"user","content":f"Target role: {target_role}\nQuestion: {question}\nResume: {resume_text or 'Not provided'}"}], max_tokens=1000, temperature=.6)
