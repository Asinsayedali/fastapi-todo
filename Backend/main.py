from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import database
import schemas
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.post("/create")
def create_user(request:schemas.user):
    return request