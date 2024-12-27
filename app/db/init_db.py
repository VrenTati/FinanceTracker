from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.category import Category

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        await add_default_categories(conn)

async def add_default_categories(conn):
    categories = ["Їжа", "Транспорт", "Розваги", "Оренда", "Здоров'я"]
    for name in categories:
        category = Category(name=name)
        conn.add(category)
    await conn.commit()
