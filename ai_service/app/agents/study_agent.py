from app.llm.client import get_completion
async def generate_study_plan(topic: str, current_level: str, weeks: int) -> str:
    return await get_completion("You are NexaMind. Produce a realistic markdown study plan: a heading per week, 3-5 concrete tasks and a readiness check. No filler.", [{"role":"user","content":f"Topic: {topic}\nLevel: {current_level}\nWeeks: {weeks}"}], max_tokens=1800, temperature=.5)
