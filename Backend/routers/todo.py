from fastapi import APIRouter, status, HTTPException, Depends
from ..database import SessionDep
from sqlmodel import select
from ..routers import authentication
from ..password import get_hashed_password, verify_password
from .. import models

router = APIRouter(
    prefix="/todo",
    tags=["Todo"]
)

@router.post("/create",response_model=models.TodoRead,status_code= status.HTTP_201_CREATED)
def create_todo(db: SessionDep, request: models.TodoCreate,current_user: models.User = Depends(authentication.get_current_user)):
    todo = models.Todo(title=request.title, description=request.description, created_at=request.created_at, due_time=request.due_time, user_id=request.user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo