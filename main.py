from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import init_db, SessionDep

about_me = {
        "name": "John Doe",
        "age": 30,
        "bio": "Software developer with a passion for learning new technologies."
    }

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.get("/")
def index(session: SessionDep):
    return {f"status connected to db with {session}"}


@app.get("/about")
def about():
    return about_me["bio"]

@app.get("/blog/{blog_id}")
def blog(blog_id: int):
    return {"blog_id": blog_id, "title": "My Blog", "content": "This is my first blog post."}

class Item(BaseModel):
    name : str
    id : int
    textfield : str | None = None

@app.post("/item")
async def item(item:Item):
    return item