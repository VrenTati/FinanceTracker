from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from core.models import UserCategory, Transaction
from core.models.category import Category
from core.schemas.category import BaseCategoryCreate, BaseCategoryUpdate
from core.types.user_id import UserIdType


class CategoryService:
    @staticmethod
    async def get_all_categories(db: AsyncSession):
        result = await db.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def get_visible_categories(db: AsyncSession, user_id: UserIdType):
        result = await db.execute(
            select(UserCategory)
            .join(Category)
            .where(UserCategory.user_id == user_id, UserCategory.hidden == False)
        )
        return result.scalars().all()

    @staticmethod
    async def create_category(db: AsyncSession, category_data: BaseCategoryCreate):
        existing = await db.execute(
            select(Category).where(Category.name == category_data.name)
        )
        if existing.scalar():
            raise HTTPException(status_code=400, detail="Category already exists")
        new_category = Category(**category_data.dict())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return new_category

    @staticmethod
    async def update_category(
        db: AsyncSession, category_id: int, category_data: BaseCategoryUpdate
    ):
        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        for key, value in category_data.dict(exclude_unset=True).items():
            setattr(category, key, value)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete_category(db: AsyncSession, category_id: int):
        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await db.delete(category)
        await db.commit()
        return {"detail": "Category deleted"}

    @staticmethod
    async def get_default_category(
        db: AsyncSession, user_id: UserIdType
    ) -> UserCategory:
        default_category = await db.execute(
            select(UserCategory)
            .join(Category)
            .where(UserCategory.user_id == user_id, Category.name == "No category")
        )
        return default_category.scalar_one_or_none()

    # TODO: Refactor in separate user_category service?
    @staticmethod
    async def delete_user_category(db: AsyncSession, user_category_id: int) -> None:
        user_category = await db.execute(
            select(UserCategory).where(UserCategory.id == user_category_id)
        )
        user_category = user_category.scalar_one_or_none()

        if not user_category:
            raise HTTPException(status_code=404, detail="Category not found")

        user_category.hidden = True

        default_category = await CategoryService.get_default_category(
            db, user_category.user_id
        )
        if not default_category:
            raise HTTPException(status_code=404, detail="Default category not found")

        await db.execute(
            update(Transaction)
            .where(
                Transaction.user_id == user_category.user_id,
                Transaction.user_category_id == user_category.category_id,
            )
            .values(category_id=default_category.category_id)
        )

        await db.commit()
