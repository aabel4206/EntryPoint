from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models

router = APIRouter(
    prefix="/api/demo",
    tags=["Demo"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/student")
def create_demo_student(db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == "demo.student@txst.edu"
    ).first()

    if existing_user:
        existing_profile = db.query(models.StudentProfile).filter(
            models.StudentProfile.user_id == existing_user.user_id
        ).first()

        return {
            "user_id": existing_user.user_id,
            "profile_id": existing_profile.profile_id
        }

    user = models.User(
        first_name="Demo",
        last_name="Student",
        email="demo.student@txst.edu",
        password_hash="demo",
        role="student"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    profile = models.StudentProfile(
        user_id=user.user_id,
        student_type="international",
        major="Computer Science",
        is_international=True
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "user_id": user.user_id,
        "profile_id": profile.profile_id
    }