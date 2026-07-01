from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.page_monitor import check_page
from app import models

router = APIRouter(
    prefix="/api/monitoring",
    tags=["Monitoring"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/check")
def monitor_page(url: str):
    return check_page(url)


@router.post("/demo-change/{resource_id}")
def create_demo_change(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(
        models.Resource.resource_id == resource_id
    ).first()

    if not resource:
        return {"error": "Resource not found"}

    subscriptions = db.query(models.StudentResourceSubscription).filter(
        models.StudentResourceSubscription.resource_id == resource_id
    ).all()

    created_notifications = []

    for subscription in subscriptions:
        notification = models.Notification(
            profile_id=subscription.profile_id,
            resource_id=resource.resource_id,
            title=f"{resource.title} update detected",
            message=f"A transportation resource you follow has changed: {resource.title}. Please review the latest information.",
            is_read=False
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)
        created_notifications.append(notification.notification_id)

    return {
        "resource_id": resource_id,
        "resource_title": resource.title,
        "affected_students": len(subscriptions),
        "created_notifications": created_notifications
    }