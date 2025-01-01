from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from core.initializers import initialize_default_categories
from core.models import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with db_helper.session_factory() as session:
        await initialize_default_categories(session)
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)

main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
