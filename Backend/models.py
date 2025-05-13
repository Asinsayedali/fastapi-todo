from sqlmodel import Field, Session, create_engine, SQLModel, select
from datetime import datetime
# User Table
class User(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    password: str 
    email: str = Field(unique=True, index=True)


#user API endpoint schemas
class UserRead(SQLModel):
    name: str
    email: str
    id : int

class UserCreate(SQLModel):
    name: str
    email: str
    password: str    

#to-do Talbe
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    due_time: datetime
    completed: bool = Field(default=False)
    completed_at: datetime | None = None
    user_id: int = Field(foreign_key="user.id")

#login schema
class Login(SQLModel):
    username: str
    password: str

#token schema
class Token(SQLModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str

class TokenData(SQLModel):
    username: str
    token_type: str

