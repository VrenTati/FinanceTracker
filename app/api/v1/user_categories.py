from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User
from core.models.db_helper import db_helper
from core.services.category_service import CategoryService
from .fastapi_users import current_user

router = APIRouter(
    prefix=settings.api.v1.user_categories,
)


@router.delete("/{user_category_id}")
async def delete_category(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    user_category_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await CategoryService.delete_user_category(db, user_category_id)
