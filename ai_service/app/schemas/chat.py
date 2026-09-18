from typing import Literal
from pydantic import BaseModel, Field

class ChatMessageIn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=20_000)

class ChatRequest(BaseModel):
    user_id: int = Field(gt=0)
    question: str = Field(min_length=1, max_length=20_000)
    history: list[ChatMessageIn] = Field(default_factory=list, max_length=15)
    document_id: int | None = Field(default=None, gt=0)

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict] = Field(default_factory=list)
