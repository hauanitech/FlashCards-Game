import uuid

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from typing import Optional

from api.base.models import TableBase


class FlashCardBase(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, max_length=300)
    recto: str = Field(min_length=1, max_length=30)
    verso: str = Field(min_length=1, max_length=30)
    is_public: bool = Field(default=True)

class FlashCards(TableBase):
    __tablename__ = "flashcards"
    name = Column(String)
    description = Column(String)
    recto = Column(String)
    verso = Column(String)
    is_public = Column(Boolean, default=True)

    lessons = relationship(
        "Lessons",
        secondary="lesson_flashcard",
        back_populates="flashcards"
    )