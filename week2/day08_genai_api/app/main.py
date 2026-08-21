from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session

from .database import Base
from .database import engine
from .database import get_db
from .llm import MODEL_NAME
from .llm import generate_response
from .models import Conversation
from .models import Message
from .schemas import GenerateRequest
from .schemas import GenerateResponse
from .schemas import MessageResponse


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Day 8 GenAI API",
    description="LLM + FastAPI + PostgreSQL",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Day 8 GenAI API is running"
    }


@app.post(
    "/generate",
    response_model=GenerateResponse
)
def generate(
    request: GenerateRequest,
    db: Session = Depends(get_db)
):

    # Check whether conversation exists
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == request.conversation_id
        )
        .first()
    )

    # Create conversation if it does not exist
    if conversation is None:

        conversation = Conversation(
            id=request.conversation_id,
            title="AI Conversation",
            type="private"
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = Message(
        conversation_id=request.conversation_id,
        role="user",
        content=request.prompt,
        metadata={}
    )

    db.add(user_message)
    db.commit()

    # Call LLM
    answer = generate_response(request.prompt)

    # Save assistant message
    assistant_message = Message(
        conversation_id=request.conversation_id,
        role="assistant",
        content=answer,
        metadata={
            "model": MODEL_NAME,
            "temperature": 0.2
        }
    )

    db.add(assistant_message)
    db.commit()

    return GenerateResponse(
        conversation_id=request.conversation_id,
        answer=answer,
        model=MODEL_NAME,
        success=True
    )


@app.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db)
):

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at)
        .all()
    )

    return [
        MessageResponse(
            id=str(message.id),
            conversation_id=str(message.conversation_id),
            role=message.role,
            content=message.content,
            metadata=message.message_metadata
        )
        for message in messages
    ]