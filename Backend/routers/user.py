from fastapi import APIRouter, status, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import List
from ..db import models
from ..db.database import SessionDep
from sqlmodel import select
from ..routers import authentication
from fastapi.security import OAuth2PasswordRequestForm
from ..password import get_hashed_password
from .. import password

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
    access_token = authentication.create_access_token(
        data={"sub": user.email}
    )
    return models.Token(access_token=access_token, token_type="bearer")

class ConnectionSetup:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket:WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, websocket:WebSocket, message: str):
        for connection in self.active_connections:
            if connection!= websocket:
               await connection.send_text(message)
    
connection_manager = ConnectionSetup()

@router.websocket("/{user_id}/Chatroom")
async def chatroom_endpoint(websocket: WebSocket, user_id: int, db: SessionDep):
    await connection_manager.connect(websocket)
    user = db.exec(select(models.User).where(models.User.id==user_id)).first()
    username = user.name if user else f"user#{user_id}"
    await connection_manager.broadcast(f"{username} has joined the room.")
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(message=data, websocket=websocket)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
