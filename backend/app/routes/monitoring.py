from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal
from app.services.ai_change_summary import (
    OLLAMA_MODEL,
    summarize_page_change,
)
from app.services.page_monitor import check_page


router = APIRouter(
    prefix="/api/monitoring",
    tags=["Monitoring"],
)


class LocalAISummaryRequest(BaseModel):
    page_title: str
    old_text: str
    new_text: str


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/pages",
    response_model=schemas.MonitoredPageResponse,
)
def create_monitored_page(
    page: schemas.MonitoredPageCreate,
    db: Session = Depends(get_db),
):
    resource = db.query(models.Resource).filter(
        models.Resource.resource_id == page.resource_id
    ).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    category = db.query(models.ResourceCategory).filter(
        models.ResourceCategory.category_id == page.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    existing_page = db.query(models.MonitoredPage).filter(
        models.MonitoredPage.url == page.url
    ).first()

    if existing_page:
        return existing_page

    monitored_page = models.MonitoredPage(
        resource_id=page.resource_id,
        category_id=page.category_id,
        title=page.title,
        url=page.url,
        active=True,
    )

    db.add(monitored_page)
    db.commit()
    db.refresh(monitored_page)

    return monitored_page


@router.get(
    "/pages",
    response_model=list[schemas.MonitoredPageResponse],
)
def get_monitored_pages(
    db: Session = Depends(get_db),
):
    return db.query(models.MonitoredPage).all()


@router.get(
    "/changes",
    response_model=list[schemas.PageChangeLogResponse],
)
def get_change_logs(
    db: Session = Depends(get_db),
):
    return db.query(models.PageChangeLog).order_by(
        models.PageChangeLog.detected_at.desc()
    ).all()


@router.post("/check/{page_id}")
def check_monitored_page(
    page_id: int,
    db: Session = Depends(get_db),
):
    page = db.query(models.MonitoredPage).filter(
        models.MonitoredPage.page_id == page_id
    ).first()

    if not page:
        raise HTTPException(
            status_code=404,
            detail="Monitored page not found",
        )

    result = check_page(page.url)

    new_hash = result["content_hash"]
    new_text = result["content_text"]

    previous_hash = page.last_content_hash
    previous_text = page.last_content_text

    page.last_checked_at = datetime.now(timezone.utc)

    # First check: store the initial baseline.
    if previous_hash is None or previous_text is None:
        page.last_content_hash = new_hash
        page.last_content_text = new_text

        db.commit()
        db.refresh(page)

        return {
            "page_id": page.page_id,
            "url": page.url,
            "changed": False,
            "message": "Initial content baseline stored.",
            "content_hash": new_hash,
        }

    # The page content has not changed.
    if previous_hash == new_hash:
        db.commit()

        return {
            "page_id": page.page_id,
            "url": page.url,
            "changed": False,
            "message": "No change detected.",
            "content_hash": new_hash,
        }

    # The page changed. Generate a local AI summary.
    ai_summary = summarize_page_change(
        page_title=page.title,
        old_text=previous_text,
        new_text=new_text,
    )

    change_log = models.PageChangeLog(
        page_id=page.page_id,
        previous_content_hash=previous_hash,
        new_content_hash=new_hash,
        change_summary=ai_summary,
        importance_level="medium",
        reviewed_by_admin=False,
    )

    db.add(change_log)
    db.flush()

    subscriptions = db.query(
        models.StudentResourceSubscription
    ).filter(
        models.StudentResourceSubscription.resource_id
        == page.resource_id
    ).all()

    notifications = []

    for subscription in subscriptions:
        notification = models.Notification(
            profile_id=subscription.profile_id,
            resource_id=page.resource_id,
            change_id=change_log.change_id,
            title=f"{page.title} update",
            message=ai_summary,
            is_read=False,
        )

        db.add(notification)
        notifications.append(notification)

    page.last_content_hash = new_hash
    page.last_content_text = new_text

    db.commit()

    for notification in notifications:
        db.refresh(notification)

    return {
        "page_id": page.page_id,
        "url": page.url,
        "changed": True,
        "change_id": change_log.change_id,
        "ai_summary": ai_summary,
        "affected_students": len(subscriptions),
        "created_notifications": [
            notification.notification_id
            for notification in notifications
        ],
    }


@router.get("/check-url")
def check_url_once(url: str):
    return check_page(url)


@router.post("/local-ai-summary-demo")
def local_ai_summary_demo(
    request: LocalAISummaryRequest,
):
    summary = summarize_page_change(
        page_title=request.page_title,
        old_text=request.old_text,
        new_text=request.new_text,
    )

    return {
        "page_title": request.page_title,
        "model": OLLAMA_MODEL,
        "runs_locally": True,
        "summary": summary,
    }