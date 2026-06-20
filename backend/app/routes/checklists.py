from fastapi import APIRouter
from app.services.checklist_generator import generate_transportation_checklist

router = APIRouter(
    prefix="/api/checklists",
    tags=["Checklists"]
)


@router.get("/transportation")
def get_transportation_checklist(is_international: bool = True):
    return {
        "student_type": "international" if is_international else "domestic",
        "domain": "transportation",
        "checklist": generate_transportation_checklist(is_international)
    }