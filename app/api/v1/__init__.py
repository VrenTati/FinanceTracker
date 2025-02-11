from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .categories import router as categories_router
from .reports import router as reports_router
from .transactions import router as transactions_router
from .user_categories import router as user_categories_router
from .users import router as users_router

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(auth_router, tags=["auth"])
router.include_router(users_router, tags=["users"])
router.include_router(categories_router, tags=["categories"])
router.include_router(transactions_router, tags=["transactions"])
router.include_router(reports_router, tags=["reports"])
router.include_router(user_categories_router, tags=["user_category"])
