from typing import Any

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    conversation_id: str
    prompt: str


class GenerateResponse(BaseModel):
    conversation_id: str
    answer: str
    model: str
    success: bool


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    metadata: dict[str, Any] | None = None