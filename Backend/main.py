from fastapi import FastAPI
from contextlib import asynccontextmanager
from Backend.database import init_db
from .routers import user


@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(user.router)



