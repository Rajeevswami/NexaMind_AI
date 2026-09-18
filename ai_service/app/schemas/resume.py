from pydantic import BaseModel, Field
class ResumeAnalyzeRequest(BaseModel): user_id:int=Field(gt=0); resume_text:str=Field(min_length=1); target_role:str|None=None
class ResumeAnalyzeResponse(BaseModel): strengths:list[str]; gaps:list[str]; suggested_improvements:list[str]; ats_notes:str; overall_summary:str
class StudyPlanRequest(BaseModel): user_id:int=Field(gt=0); topic:str=Field(min_length=1); current_level:str="beginner"; weeks:int=Field(default=4, ge=1, le=52)
class StudyPlanResponse(BaseModel): plan_markdown:str
class CareerAdviceRequest(BaseModel): user_id:int=Field(gt=0); target_role:str=Field(min_length=1); question:str=Field(min_length=1); resume_text:str|None=None
class CareerAdviceResponse(BaseModel): answer:str
