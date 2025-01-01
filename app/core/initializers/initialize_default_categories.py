from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Category

async def initialize_default_categories(db: AsyncSession):
    default_categories = settings.category.default_categories
    for category_name in default_categories:
        existing_category = await db.execute(
            select(Category).where(Category.name == category_name)
        )
        if not existing_category.scalar_one_or_none():
            db.add(Category(name=category_name, default=True))
    await db.commit()
