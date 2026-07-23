from datetime import datetime, timezone
from types import SimpleNamespace

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

    # Optional demo-personalization fields.
    category_name: str = "Transportation"
    student_type: str = "Undergraduate"
    major: str | None = None
    is_international: bool = True


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_category_name(category) -> str:
    """
    Safely retrieve a category name even if the model uses a different
    column name.
    """

    if category is None:
        return "University resource"

    possible_names = (
        "category_name",
        "name",
        "title",
    )

    for attribute_name in possible_names:
        value = getattr(category, attribute_name, None)

        if value:
            return str(value)

    return "University resource"


def build_personalized_notification(
    page_title: str,
    ai_summary: str,
    student_profile,
    category,
) -> str:
    """
    Create a student-facing notification using the AI-generated factual
    summary, the resource category, the student's subscription, and the
    profile information currently stored in the database.
    """

    category_name = get_category_name(category)
    category_text = category_name.lower()
    page_title_text = page_title.lower()

    student_type = (
        getattr(student_profile, "student_type", None)
        if student_profile
        else None
    )

    major = (
        getattr(student_profile, "major", None)
        if student_profile
        else None
    )

    is_international = bool(
        getattr(student_profile, "is_international", False)
        if student_profile
        else False
    )

    why_it_matters = (
        f"You subscribed to this {category_name.lower()} resource, "
        "so EntryPoint identified this update as relevant to you."
    )

    profile_context = []

    if student_type:
        profile_context.append(
            f"Your profile identifies you as a {student_type.lower()} student."
        )

    if is_international:
        profile_context.append(
            "Because you are an international student, changes to university "
            "services, requirements, and onboarding resources may require "
            "additional planning."
        )

    if major:
        profile_context.append(
            f"Your saved academic program is {major}."
        )

    if profile_context:
        why_it_matters = (
            f"{why_it_matters} {' '.join(profile_context)}"
        )

    recommended_action = (
        "Review the updated webpage and confirm whether the change affects "
        "any upcoming plans, requirements, or deadlines."
    )

    if (
        "transport" in category_text
        or "shuttle" in category_text
        or "bus" in category_text
        or "transport" in page_title_text
        or "shuttle" in page_title_text
        or "bus" in page_title_text
    ):
        recommended_action = (
            "Check the updated route and operating schedule before your next "
            "trip to campus. If service is unavailable when you need it, "
            "consider leaving earlier, using another route, carpooling, "
            "rideshare, or arranging another form of transportation."
        )

    elif (
        "accommodation" in category_text
        or "housing" in category_text
        or "apartment" in category_text
        or "housing" in page_title_text
    ):
        recommended_action = (
            "Review the updated housing information and verify whether any "
            "deadlines, prices, eligibility requirements, documents, or "
            "availability details have changed."
        )

    elif (
        "international" in category_text
        or "immigration" in category_text
        or "visa" in category_text
    ):
        recommended_action = (
            "Review the official update carefully and verify whether you need "
            "to submit documents, contact the international office, or take "
            "action before a stated deadline."
        )

    elif (
        "financial" in category_text
        or "tuition" in category_text
        or "fee" in category_text
    ):
        recommended_action = (
            "Review the new financial information and verify whether the "
            "change affects your balance, payment deadline, required forms, "
            "or financial planning."
        )

    return (
        f"What changed:\n"
        f"{ai_summary}\n\n"
        f"Why this matters to you:\n"
        f"{why_it_matters}\n\n"
        f"Recommended action:\n"
        f"{recommended_action}"
    )


@router.post(
    "/pages",
    response_model=schemas.MonitoredPageResponse,
)
def create_monitored_page(
    page: schemas.MonitoredPageCreate,
    db: Session = Depends(get_db),
):
    resource = (
        db.query(models.Resource)
        .filter(
            models.Resource.resource_id == page.resource_id
        )
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    category = (
        db.query(models.ResourceCategory)
        .filter(
            models.ResourceCategory.category_id == page.category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    existing_page = (
        db.query(models.MonitoredPage)
        .filter(
            models.MonitoredPage.url == page.url
        )
        .first()
    )

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
    return (
        db.query(models.PageChangeLog)
        .order_by(
            models.PageChangeLog.detected_at.desc()
        )
        .all()
    )


@router.post("/check/{page_id}")
def check_monitored_page(
    page_id: int,
    db: Session = Depends(get_db),
):
    page = (
        db.query(models.MonitoredPage)
        .filter(
            models.MonitoredPage.page_id == page_id
        )
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=404,
            detail="Monitored page not found",
        )

    category = (
        db.query(models.ResourceCategory)
        .filter(
            models.ResourceCategory.category_id == page.category_id
        )
        .first()
    )

    result = check_page(page.url)

    new_hash = result["content_hash"]
    new_text = result["content_text"]

    previous_hash = page.last_content_hash
    previous_text = page.last_content_text

    page.last_checked_at = datetime.now(timezone.utc)

    # First check: store the initial page content as the baseline.
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

    # No meaningful page-content change was detected.
    if previous_hash == new_hash:
        db.commit()

        return {
            "page_id": page.page_id,
            "url": page.url,
            "changed": False,
            "message": "No change detected.",
            "content_hash": new_hash,
        }

    # A change was detected. Generate a factual local-AI summary.
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

    subscriptions = (
        db.query(models.StudentResourceSubscription)
        .filter(
            models.StudentResourceSubscription.resource_id
            == page.resource_id
        )
        .all()
    )

    notifications = []

    for subscription in subscriptions:
        student_profile = (
            db.query(models.StudentProfile)
            .filter(
                models.StudentProfile.profile_id
                == subscription.profile_id
            )
            .first()
        )

        personalized_message = build_personalized_notification(
            page_title=page.title,
            ai_summary=ai_summary,
            student_profile=student_profile,
            category=category,
        )

        notification = models.Notification(
            profile_id=subscription.profile_id,
            resource_id=page.resource_id,
            change_id=change_log.change_id,
            title=f"EntryPoint AI Assistant: {page.title}",
            message=personalized_message,
            is_read=False,
        )

        db.add(notification)
        notifications.append(notification)

    page.last_content_hash = new_hash
    page.last_content_text = new_text

    db.commit()

    db.refresh(change_log)

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

    # Create temporary objects so the demo uses the same personalization
    # logic as real database notifications.
    demo_student_profile = SimpleNamespace(
        student_type=request.student_type,
        major=request.major,
        is_international=request.is_international,
    )

    demo_category = SimpleNamespace(
        category_name=request.category_name,
    )

    personalized_notification = build_personalized_notification(
        page_title=request.page_title,
        ai_summary=summary,
        student_profile=demo_student_profile,
        category=demo_category,
    )

    return {
        "page_title": request.page_title,
        "model": OLLAMA_MODEL,
        "runs_locally": True,
        "summary": summary,
        "personalized_notification": personalized_notification,
        "student_context": {
            "student_type": request.student_type,
            "major": request.major,
            "is_international": request.is_international,
            "subscribed_category": request.category_name,
        },
    }