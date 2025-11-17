from fastapi import FastAPI
from sqlmodel import SQLModel
from api.urls.users import users_router
from api.urls.players import players_router
from api.urls.items import items_router
from api.config import VERSION

from api.db import engine


app = FastAPI( version = VERSION )


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router( users_router )
app.include_router( players_router )
app.include_router( items_router )


@app.get('/')
async def home() -> dict:
    return { 'message': 'Hello world!' }

