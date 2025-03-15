from fastapi import APIRouter
from .views import router

todo_router = APIRouter()
todo_router.include_router(router)
