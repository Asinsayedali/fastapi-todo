from fastapi import APIRouter, status, HTTPException
from ..database import SessionDep
from sqlmodel import select
from ..password import get_hashed_password, verify_password
from .. import models

router = APIRouter()
    
@router.post("/signup",response_model= models.UserRead,status_code=status.HTTP_201_CREATED, tags=["Users"])
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

@router.get("/user/{id}",response_model = models.UserRead,tags=["Users"])
def get_user_data(id: int,db: SessionDep):
    user = db.exec(select(models.User).where(models.User.id==id)).first()
    if not user:
         raise HTTPException(status_code=400, detail = "User does not exists!") 
    return user