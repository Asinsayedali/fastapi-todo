from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlmodel import select
from .. import models,password
from dotenv import load_dotenv
from ..database import SessionDep, get_session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
load_dotenv()
router = APIRouter(
    prefix="/authenticate",
    tags=["authentication"]
)
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
        user = db.exec(select(models.User).where(models.User.email == token_data.username)).first()
        return user
    except JWTError:
        raise credentials_exception

@router.post("/login")  
def login( db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.exec(select(models.User).where(models.User.email==form_data.username)).first()
    if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not password.verify_password(form_data.password,user.password):
        raise HTTPException(status_code=400, detail = "Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return models.Token(access_token=access_token, token_type="bearer")