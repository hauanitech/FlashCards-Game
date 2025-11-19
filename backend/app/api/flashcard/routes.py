import uuid

from datetime import datetime
from fastapi import APIRouter, HTTPException
from api.flashcard.models import FlashCardBase, FlashCards
from core.security import UserDep, AdminDep, SuperDep, SessionDep, is_owner


router = APIRouter(prefix="/flashcard", tags=["flashcard"])


@router.get("/get_my_flashcards")
async def get_my_flashcards(*, Session: SessionDep, User: UserDep):
    db_flashcard = (
        Session.query(FlashCards)
        .filter(FlashCards.created_by == uuid.UUID(User["id"]))
        .all()
    )
    return {"data": db_flashcard}


@router.post("/create_flashcard")
async def create_flashcard(
    *, Session: SessionDep, User: UserDep, FlashCard: FlashCardBase
):
    db_flashcard = FlashCards(
        id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by=uuid.UUID(User["id"]),
        name=FlashCard.name,
        description=FlashCard.description,
        recto=FlashCard.recto,
        verso=FlashCard.verso,
        is_public=FlashCard.is_public,
        lesson_ids=[str(id) for id in FlashCard.lesson_ids],
        shared_with_users=[str(id) for id in FlashCard.shared_with_users],
    )
    Session.add(db_flashcard)
    Session.commit()
    return {"data": "Flash Created Successfully"}


@router.get("/get_all_flashcards")
async def get_all_flashcards(
    *,
    Session: SessionDep,
    User: AdminDep,
):
    db_flashcards = Session.query(FlashCards).all()
    return {"data": db_flashcards}


@router.delete("/delete_flashcard/{id}")
async def delete_flashcard(*, Session: SessionDep, User: UserDep, id: uuid.UUID):
    db_flashcard = Session.query(FlashCards).filter(FlashCards.id == id).first()
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="FlashCard Not Found")
    if not is_owner(User, db_flashcard, Session):
        raise HTTPException(status_code=403, detail="Forbidden")

    Session.delete(db_flashcard)
    Session.commit()

    return {"data": "FlashCard Deleted Successfully"}


@router.get("/get_flashcard_by_id/{id}")
async def get_flashcard_by_id(*, Session: SessionDep, User: UserDep, id: uuid.UUID):
    db_flashcard = Session.query(FlashCards).filter(FlashCards.id == id).first()
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="FlashCard Not Found")
    if not is_owner(User, db_flashcard, Session):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data": db_flashcard}


@router.get("/update_flashcard/{id}")
async def update_flashcard(
    *, Session: SessionDep, User: UserDep, id: uuid.UUID, data: FlashCardBase
):
    db_flashcard = Session.query(FlashCards).filter(FlashCards.id == id).first()
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="FlashCard Not Found")
    if not is_owner(User, db_flashcard, Session):
        raise HTTPException(status_code=403, detail="Forbidden")
    db_flashcard.description = data.description
    db_flashcard.updated_at = datetime.now()
    db_flashcard.is_public = data.is_public
    db_flashcard.name = data.name
    db_flashcard.recto = data.recto
    db_flashcard.verso = data.verso

    Session.commit()
    return {"data": "FlashCard Updated Successfully"}
