from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{profile_id}", response_model=list[schemas.NotificationResponse])
def get_student_notifications(profile_id: int, db: Session = Depends(get_db)):
    return db.query(models.Notification).filter(
        models.Notification.profile_id == profile_id
    ).all()