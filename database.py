import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, create_engine, SQLModel, select
load_dotenv()


DB_URL = os.getenv("DATABASE_URL")  

if not DB_URL:
    print("Database url not found in .env file!")


engine = create_engine(DB_URL,echo=True)

def get_session():
    with Session(engine) as session:
        yield session
    
SessionDep = Annotated[Session, Depends(get_session)]

def init_db():
    SQLModel.metadata.create_all(engine)