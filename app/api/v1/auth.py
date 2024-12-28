from fastapi import APIRouter

from api.dependecies.auth.backend import authentication_backend
from api.v1.fastapi_users import fastapi_users
from core.config import settings
from core.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_auth_router(authentication_backend),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
