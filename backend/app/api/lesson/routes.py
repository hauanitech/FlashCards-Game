import uuid

from datetime import datetime
from fastapi import APIRouter, HTTPException

from core.security import UserDep, SessionDep, AdminDep, SuperDep, is_owner
from api.lesson.models import LessonBase, Lessons
from api.base.routes import default_post


router = APIRouter(
    prefix="/lesson",
    tags=["lesson"]
)


@router.get("/get_lessons")
async def get_lessons(
    *,
    Session: SessionDep,
    User: AdminDep
):
    return {"data" : Session.query(Lessons).all()}


@router.get("/get_lesson_by_id/{id}")
async def get_lesson_by_id(
    *,
    Session: SessionDep,
    User: UserDep,
    id: uuid.UUID
):
    db_lesson = Session.query(Lessons).filter(Lessons.id == id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson Not Found")
    if not is_owner(User, db_lesson, Session):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data" : db_lesson}


@router.post("/create_lesson")
async def create_lesson(
    *,
    Session: SessionDep,
    User: UserDep,
    data: LessonBase
):
    db_lesson = default_post(User, Lessons)
    db_lesson.content = data.content
    db_lesson.name = data.name

    Session.add(db_lesson)
    Session.commit()
    return {"data" : "Lesson Created Successfully"}


@router.put("/update_lesson/{id}")
async def update_lesson(
    *,
    User: UserDep,
    Session: SessionDep,
    id: uuid.UUID,
    data: LessonBase
):
    db_lesson = Session.query(Lessons).filter(Lessons.id == id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson Not Found")
    if not is_owner(User, db_lesson, Session):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    db_lesson.content = data.content
    db_lesson.name = data.name
    db_lesson.updated_at = datetime.now()
    
    Session.commit()
    return {"data" : "Lesson Updated Successfully"}


@router.delete("/delete_lesson/{id}")
async def delete_lesson(
    *,
    Session: SessionDep,
    User: UserDep,
    id: uuid.UUID
):
    db_lesson = Session.query(Lessons).filter(Lessons.id == id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson Not Found")
    if not is_owner(User, db_lesson, Session):
        raise HTTPException(status_code=403, detail="Forbidden")
    Session.delete(db_lesson)
    Session.commit()
    return {"data" : "Lesson Deleted Successfully"}


@router.get("/get_my_lessons")
async def get_my_lessons(
    *,
    Session: SessionDep,
    User: UserDep
):
    return {"data" : Session.query(Lessons).filter(Lessons.created_by == uuid.UUID(User["id"])).all()}