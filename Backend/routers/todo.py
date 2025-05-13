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

@router.post("/create")
def create_todo():
    return "todo creation end point"