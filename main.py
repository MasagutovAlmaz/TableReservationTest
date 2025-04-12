from contextlib import asynccontextmanager
from src.api.reservation import router as reservation_router
from src.api.table import router as table_router
from fastapi import FastAPI
import uvicorn

from src.db.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db()
app = FastAPI(lifespan=lifespan)

app.include_router(table_router)
app.include_router(reservation_router)


