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

@router.delete("/todos/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_todo(
    todo_id: int,
    db: SessionDep,
    current_user: models.User = Depends(authentication.get_current_user),
):
    todo = db.exec(select(models.Todo).where(models.Todo.id == todo_id, models.Todo.user_id == current_user.id)).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return  {"details":"Todo deleted"}