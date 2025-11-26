from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Table, UUID, ForeignKey
from sqlalchemy.orm import relationship

from api.base.models import TableBase
from database import Base


class LessonBase(BaseModel):
    name: str = Field(description="Lesson's Name", max_length=50)
    content: str = Field(description="Lesson Content", max_length=2000)


lesson_flashcard = Table(
    'lesson_flashcard',
    Base.metadata,
    Column('lessons_id', UUID, ForeignKey('lessons.id', ondelete='CASCADE'), primary_key=True),
    Column('flashcards_id', UUID, ForeignKey('flashcards.id', ondelete='CASCADE'), primary_key=True)
)


class Lessons(TableBase):
    __tablename__ = "lessons"

    name = Column(String)
    content = Column(String)

    flashcards = relationship(
        "FlashCards",
        secondary=lesson_flashcard,
        back_populates="lessons"
    )
    
