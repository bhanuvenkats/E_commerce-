from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
async def dashboard_summary():
    return {
        "total_products": 0,
        "total_categories": 0,
        "active_users": 1
    }