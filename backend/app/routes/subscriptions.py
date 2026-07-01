from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas

router = APIRouter(
    prefix="/api/subscriptions",
    tags=["Subscriptions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.SubscriptionResponse)
def subscribe_to_resource(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    profile = db.query(models.StudentProfile).filter(
        models.StudentProfile.profile_id == subscription.profile_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    resource = db.query(models.Resource).filter(
        models.Resource.resource_id == subscription.resource_id
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    existing_subscription = db.query(models.StudentResourceSubscription).filter(
        models.StudentResourceSubscription.profile_id == subscription.profile_id,
        models.StudentResourceSubscription.resource_id == subscription.resource_id
    ).first()

    if existing_subscription:
        return existing_subscription

    new_subscription = models.StudentResourceSubscription(
        profile_id=subscription.profile_id,
        resource_id=subscription.resource_id
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


@router.get("/{profile_id}", response_model=list[schemas.SubscriptionResponse])
def get_student_subscriptions(profile_id: int, db: Session = Depends(get_db)):
    return db.query(models.StudentResourceSubscription).filter(
        models.StudentResourceSubscription.profile_id == profile_id
    ).all()