import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from .database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    title = Column(
        String(200),
        nullable=True
    )

    type = Column(
        String(20),
        nullable=False,
        default="private"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    message_metadata = Column(
        "metadata",
        JSONB,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )