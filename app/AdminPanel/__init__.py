from fastapi import APIRouter

from app.AdminPanel.Admin import router as AdminRouter

router = APIRouter()

router.include_router(AdminRouter)