from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models.category import Category
from core.schemas.category import BaseCategoryCreate, BaseCategoryUpdate

class CategoryService:
    @staticmethod
    async def get_categories(db: AsyncSession):
        result = await db.execute(select(Category))
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
