from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.page_monitor import check_page
from app import models, schemas

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


@router.post("/pages", response_model=schemas.MonitoredPageResponse)
def create_monitored_page(page: schemas.MonitoredPageCreate, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(
        models.Resource.resource_id == page.resource_id
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    category = db.query(models.ResourceCategory).filter(
        models.ResourceCategory.category_id == page.category_id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing = db.query(models.MonitoredPage).filter(
        models.MonitoredPage.url == page.url
    ).first()

    if existing:
        return existing

    new_page = models.MonitoredPage(
        resource_id=page.resource_id,
        category_id=page.category_id,
        title=page.title,
        url=page.url,
        active=True
    )

    db.add(new_page)
    db.commit()
    db.refresh(new_page)

    return new_page


@router.get("/pages", response_model=list[schemas.MonitoredPageResponse])
def get_monitored_pages(db: Session = Depends(get_db)):
    return db.query(models.MonitoredPage).all()


@router.get("/changes", response_model=list[schemas.PageChangeLogResponse])
def get_change_logs(db: Session = Depends(get_db)):
    return db.query(models.PageChangeLog).order_by(
        models.PageChangeLog.detected_at.desc()
    ).all()


@router.post("/check/{page_id}")
def check_monitored_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(models.MonitoredPage).filter(
        models.MonitoredPage.page_id == page_id
    ).first()

    if not page:
        raise HTTPException(status_code=404, detail="Monitored page not found")

    result = check_page(page.url)
    new_hash = result["content_hash"]
    previous_hash = page.last_content_hash

    page.last_checked_at = datetime.now(timezone.utc)

    if previous_hash is None:
        page.last_content_hash = new_hash
        db.commit()
        db.refresh(page)

        return {
            "page_id": page.page_id,
            "url": page.url,
            "changed": False,
            "message": "Initial hash stored.",
            "content_hash": new_hash
        }

    if previous_hash == new_hash:
        db.commit()

        return {
            "page_id": page.page_id,
            "url": page.url,
            "changed": False,
            "message": "No change detected.",
            "content_hash": new_hash
        }

    change_log = models.PageChangeLog(
        page_id=page.page_id,
        previous_content_hash=previous_hash,
        new_content_hash=new_hash,
        change_summary=f"Detected content change for {page.title}.",
        importance_level="medium",
        reviewed_by_admin=False
    )

    db.add(change_log)
    db.commit()
    db.refresh(change_log)

    page.last_content_hash = new_hash
    db.commit()

    subscriptions = db.query(models.StudentResourceSubscription).filter(
        models.StudentResourceSubscription.resource_id == page.resource_id
    ).all()

    created_notifications = []

    for subscription in subscriptions:
        notification = models.Notification(
            profile_id=subscription.profile_id,
            resource_id=page.resource_id,
            change_id=change_log.change_id,
            title=f"{page.title} update detected",
            message=f"A transportation resource you follow has changed: {page.title}. Please review the latest information.",
            is_read=False
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)
        created_notifications.append(notification.notification_id)

    return {
        "page_id": page.page_id,
        "url": page.url,
        "changed": True,
        "change_id": change_log.change_id,
        "affected_students": len(subscriptions),
        "created_notifications": created_notifications,
        "new_hash": new_hash
    }


@router.get("/check-url")
def check_url_once(url: str):
    return check_page(url)