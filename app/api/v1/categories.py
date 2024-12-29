from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User
from core.models.db_helper import db_helper
from core.schemas.category import BaseCategory, BaseCategoryCreate, BaseCategoryUpdate
from core.services.category_service import CategoryService
from .fastapi_users import current_user

router = APIRouter(
    prefix=settings.api.v1.categories,
)

@router.get("/", response_model=list[BaseCategory])
async def get_categories(
        user: Annotated[
            User,
            Depends(current_user),
        ],
        db: AsyncSession = Depends(db_helper.session_getter),
):
    return await CategoryService.get_categories(db)

@router.post("/", response_model=BaseCategory)
async def create_category(
        user: Annotated[
            User,
            Depends(current_user),
        ],
        category: BaseCategoryCreate,
        db: AsyncSession = Depends(db_helper.session_getter)
):
    return await CategoryService.create_category(db, category)

@router.put("/{category_id}", response_model=BaseCategory)
async def update_category(
        user: Annotated[
            User,
            Depends(current_user),
        ],
        category_id: int,
        category: BaseCategoryUpdate,
        db: AsyncSession = Depends(db_helper.session_getter)
):
    return await CategoryService.update_category(db, category_id, category)

@router.delete("/{category_id}")
async def delete_category(
        user: Annotated[
            User,
            Depends(current_user),
        ],
        category_id: int,
        db: AsyncSession = Depends(db_helper.session_getter)
):
    return await CategoryService.delete_category(db, category_id)
