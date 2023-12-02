from fastapi import APIRouter

from app.interfaces.rest.endpoints import (
    job, user, auth
)

api_router = APIRouter()
api_router.include_router(
    job.router,
    prefix="/jobs",
    tags=["Jobs"],
)
api_router.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
)
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)


