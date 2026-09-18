from fastapi import APIRouter, Depends, HTTPException
from app.agents.career_agent import get_career_advice
from app.agents.resume_agent import analyze_resume
from app.agents.study_agent import generate_study_plan
from app.core.security import verify_internal_key
from app.schemas.resume import *
router=APIRouter(prefix="/ai",tags=["career-tools"],dependencies=[Depends(verify_internal_key)])
@router.post("/resume/analyze",response_model=ResumeAnalyzeResponse)
async def resume_analyze(payload:ResumeAnalyzeRequest):
    try:return ResumeAnalyzeResponse(**await analyze_resume(payload.resume_text,payload.target_role))
    except Exception as error: raise HTTPException(500,"Resume analysis failed") from error
@router.post("/study-plan/generate",response_model=StudyPlanResponse)
async def study_plan(payload:StudyPlanRequest): return StudyPlanResponse(plan_markdown=await generate_study_plan(payload.topic,payload.current_level,payload.weeks))
@router.post("/career/advice",response_model=CareerAdviceResponse)
async def career_advice(payload:CareerAdviceRequest): return CareerAdviceResponse(answer=await get_career_advice(payload.question,payload.target_role,payload.resume_text))
