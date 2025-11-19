import uuid
import time

from datetime import datetime
from fastapi import FastAPI

from database import Base, engine, SessionLocal
from api.routes import router as api_router
from status.status import router as superuser_router
from api.user.models import Users
from core.security import bcrypt_context
from core.config import SUPERUSER_USERNAME, SUPERUSER_PASSWORD


app = FastAPI()


app.include_router(api_router)
app.include_router(superuser_router)


@app.on_event("startup")
def startup_event():
    """Initialize database and create superuser on startup"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            create_superuser()
            print("Database initialized successfully")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to initialize database after {max_retries} attempts: {e}")
                raise


@app.get("/")
async def root():
    return {"data": "App is running"}


def create_superuser():
    """Superuser Creation on startup function"""

    Session = SessionLocal()

    db_superuser = (
        Session.query(Users).filter(Users.username == SUPERUSER_USERNAME).first()
    )
    if db_superuser:
        return {"data": "Superuser Already Exist"}

    db_super = Users(
        id=uuid.uuid4(),
        username=SUPERUSER_USERNAME,
        hashed_password=bcrypt_context.hash(SUPERUSER_PASSWORD),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_admin=True,
        is_superuser=True,
    )

    Session.add(db_super)
    Session.commit()
    Session.close()
    return {"data": "Superuser Created Successfully"}
