from fastapi import APIRouter, status, HTTPException, Depends
from ..database import SessionDep
from sqlmodel import select
from ..routers import authentication
from ..password import get_hashed_password, verify_password
from .. import models

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/signup",response_model= models.UserRead,status_code=status.HTTP_201_CREATED)
def create_user(request:models.UserCreate, db: SessionDep):
    db_user = db.exec(select(models.User).where(models.User.email == request.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail = "User already exists!")
    hashed_password = get_hashed_password(request.password)
    user = models.User(name= request.name,password=hashed_password, email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return  user

@router.get("/{id}",response_model = models.UserRead, status_code=status.HTTP_302_FOUND)
def get_user_data(id: int, db: SessionDep, current_user: models.User = Depends(authentication.get_current_user)):
    user = db.exec(select(models.User).where(models.User.id==id)).first()
    if not user:
         raise HTTPException(status_code=400, detail = "User does not exists!") 
    return user