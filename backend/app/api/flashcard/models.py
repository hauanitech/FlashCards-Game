import uuid

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean, JSON
from typing import List, Optional

from api.base.models import TableBase


class FlashCardBase(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, max_length=300)
    recto: str = Field(min_length=1, max_length=30)
    verso: str = Field(min_length=1, max_length=30)
    is_public: bool = Field(default=True)
    lesson_ids: List[uuid.UUID] = Field(default_factory=list)
    shared_with_users: List[uuid.UUID] = Field(default_factory=list, description="Liste des IDs d'utilisateurs avec qui la flashcard est partagée")


class FlashCards(TableBase):
    __tablename__ = "flashcards"
    name = Column(String)
    description = Column(String)
    recto = Column(String)
    verso = Column(String)
    is_public = Column(Boolean, default=True)
    lesson_ids = Column(JSON, default=list)
    shared_with_users = Column(JSON, default=list)