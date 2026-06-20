from fastapi import APIRouter
from app.services.page_monitor import check_page

router = APIRouter(
    prefix="/api/monitoring",
    tags=["Monitoring"]
)


@router.get("/check")
def monitor_page(url: str):
    return check_page(url)