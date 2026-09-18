import json
from app.llm.client import get_completion
async def analyze_resume(resume_text: str, target_role: str | None = None) -> dict:
    raw = await get_completion("You are NexaMind, a precise resume reviewer. Return only valid JSON with strengths, gaps, suggested_improvements, ats_notes, and overall_summary. Reference resume facts; do not invent them.", [{"role":"user","content":f"Resume:\n{resume_text}\nTarget role: {target_role or 'Not specified'}"}], max_tokens=1500, temperature=.3)
    try: return json.loads(raw)
    except json.JSONDecodeError: return {"strengths":[],"gaps":[],"suggested_improvements":[],"ats_notes":"Structured analysis was unavailable.","overall_summary":raw[:500]}
