from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from api.urls import ( users_router, players_router, game_classes_router, location_router )

from api.urls.enemies import enemies_router
from api.urls.items import items_router
from api.urls.inventory import inventory_router
from api.urls.effects import effects_router

from api.config import VERSION, MEDIA_FOLDER
from api.db import engine


@asynccontextmanager
async def lifespan( app: FastAPI ):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI( version = VERSION, lifespan = lifespan )


app.mount( '/media', StaticFiles( directory = MEDIA_FOLDER ), name = "static" )


app.include_router( users_router )
app.include_router( players_router )
app.include_router( game_classes_router )
app.include_router( location_router )
app.include_router( items_router )
# app.include_router( enemies_router )
# app.include_router( effects_router )
# app.include_router( inventory_router )


@app.get('/')
async def home() -> dict:
    return { 'message': 'Hello world!' }
