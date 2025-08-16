from fastapi import APIRouter

from app.admin.admin import router as AdminRouter

router = APIRouter()

router.include_router(AdminRouter)