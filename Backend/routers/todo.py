from fastapi import APIRouter, status, HTTPException, Depends
from ..database import SessionDep
from sqlmodel import select
from ..routers import authentication
from ..password import get_hashed_password, verify_password
from .. import models
from datetime import datetime
import pytz

router = APIRouter(
    prefix="/todo",
    tags=["Todo"]
)

# Todo create endpoint
@router.post("/create",response_model=models.TodoRead,status_code= status.HTTP_201_CREATED)
def create_todo(db: SessionDep, request: models.TodoCreate,current_user: models.User = Depends(authentication.get_current_user)):
    todo = models.Todo(title=request.title, description=request.description, created_at=request.created_at, due_time=request.due_time, user_id=request.user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

## List todo according to status of completion and due time.
@router.get("/list",response_model=models.CategorizedTodos,status_code=status.HTTP_200_OK)
def get_todos(db:SessionDep, current_user: models.User = Depends(authentication.get_current_user)):
    todo = db.exec(select(models.Todo).where(models.Todo.user_id==current_user.id)).all()
    if not todo:
        raise HTTPException(status_code=404, detail="No data found!")
    ist_timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist_timezone)
    completed = []
    not_completed = []
    due_over = []

    for t in todo:
        due_time = t.due_time
        if due_time.tzinfo is None:
            due_time = ist_timezone.localize(due_time)

        if t.completed:
            completed.append(t)
        elif not t.completed and due_time >= now:
            not_completed.append(t)
        elif not t.completed and due_time < now:
            due_over.append(t)

    categorized = models.CategorizedTodos(
        completed=completed,
        not_completed=not_completed,
        due_over=due_over
    )

    return categorized

#update a todo with its id
@router.put("/update/{todo_id}", response_model=models.TodoRead,status_code=status.HTTP_202_ACCEPTED)
def update_todo(db:SessionDep, todo_id: int, request: models.TodoUpdate, current_user: models.User = Depends(authentication.get_current_user)):
    query = select(models.Todo).where(models.Todo.user_id==current_user.id , models.Todo.id==todo_id)
    todo = db.exec(query).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    update_data = request.dict(exclude_unset=True)
    if update_data.get("completed") and not update_data.get("completed_at"):
        update_data["completed_at"] = datetime.utcnow()
    if "description" in update_data:
        todo.description = update_data["description"]
    if "completed_at" in update_data:
        todo.completed_at = update_data["completed_at"]
    if "due_time" in update_data:
        todo.due_time = update_data["due_time"]
    if "completed" in update_data:
        todo.completed = update_data["completed"]


    db.commit()
    return todo


#Todo delete endpoint
@router.delete("/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
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