import uuid

from datetime import datetime
from fastapi import APIRouter, HTTPException
from api.flashcard.models import FlashCardBase, FlashCards
from core.security import UserDep, AdminDep, SuperDep, SessionDep


router = APIRouter(
    prefix="/flashcard",
    tags=["flashcard"]
)


@router.get("/get_my_flashcards")
async def get_my_flashcards(
    *,
    Session: SessionDep,
    User: UserDep
):
    db_flashcard = Session.query(FlashCards).filter(FlashCards.created_by == uuid.UUID(User["id"])).all()
    return {"data" : db_flashcard}


@router.post("/create_flashcard")
async def create_flashcard(
    *,
    Session: SessionDep,
    User: UserDep,
    FlashCard: FlashCardBase
):
    db_flashcard = FlashCards(
        id = uuid.uuid4(),
        created_at = datetime.now(),
        updated_at = datetime.now(),
        created_by = uuid.UUID(User["id"]),

        name = FlashCard.name,
        description = FlashCard.description,
        recto = FlashCard.recto,
        verso = FlashCard.verso,
        is_public = FlashCard.is_public,
        lesson_ids = [str(id) for id in FlashCard.lesson_ids],
        shared_with_users = [str(id) for id in FlashCard.shared_with_users]
    )
    Session.add(db_flashcard)
    Session.commit()
    return {"data" : "Flash Created Successfully"}