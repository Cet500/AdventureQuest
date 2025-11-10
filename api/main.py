from typing import Annotated

from fastapi import FastAPI, Depends, Path, HTTPException
from sqlmodel import  create_engine, SQLModel, Session
from api.urls.users import users_router
from api.config import VERSION, DB_NAME
from api.models import Player, PlayerBase, PlayerID

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


app = FastAPI( version = VERSION )


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router( users_router )


@app.get('/')
async def home() -> dict:
    return { 'message': 'Hello world 2222!' }


@app.post( '/players' )
async def create_player(
        player_base: PlayerBase,
        session: SessionDep
) -> dict:
    player = Player( nickname = player_base.nickname )

    session.add( player )
    session.commit()
    session.refresh( player )

    return { 'id': player.id }


@app.get( '/players/{player_id}' )
async def get_player(
    player_id: Annotated[ int, Path() ],
    session: SessionDep
) -> Player:
    player = session.get( Player, player_id )

    if not player:
        raise HTTPException( 404, 'Player not found' )

    return player
