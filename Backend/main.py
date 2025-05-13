from fastapi import FastAPI
from contextlib import asynccontextmanager
from Backend.database import init_db
from .routers import user, authentication, todo


@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(todo.router)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



