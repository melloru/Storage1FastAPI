from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from api import router as main_router
from core import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


web_app = FastAPI(lifespan=lifespan)

web_app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:web_app",
        host="localhost",
        port=8000,
    )
