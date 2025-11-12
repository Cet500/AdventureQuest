from typing import Annotated

from fastapi import Depends
from sqlmodel import  create_engine, Session
from api.config import DB_NAME


connect_args = {"check_same_thread": False}
engine = create_engine(
    f"sqlite:///{DB_NAME}",
    echo = True,
    connect_args = connect_args
)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
