from typing import Annotated, List

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models import GameClass, GameClassBase
from api.models.game_classes import GameClassID
from api.db import SessionDep
import logging


logger = logging.getLogger(__name__)
game_classes_router = APIRouter(prefix="/game_classes", tags=["game_classes"])


@game_classes_router.post(
    "",
    status_code=201,
    response_model=GameClassID
)
async def create_game_class(
        game_class_base: GameClassBase,
        session: SessionDep
) -> GameClassID:
    existing_game_class = session.exec(
        select(GameClass).where(GameClass.name == game_class_base.name)
    ).first()

    if existing_game_class:
        raise HTTPException(409, "GameClass with this name already exists")

    game_class = GameClass.model_validate(game_class_base.model_dump())

    session.add( game_class )
    session.commit()
    session.refresh( game_class )

    return GameClassID( id = gc.id )


@game_classes_router.get(
    "",
    status_code=200,
    response_model=List[GameClass]
)
async def get_game_classes(
        session: SessionDep
) -> List[GameClass]:
    game_classes = session.exec( select(GameClass) ).all()
    return game_classes


@game_classes_router.get(
    "/{class_id}",
    status_code=200,
    response_model=GameClass
)
async def get_game_class_by_id(
        class_id: Annotated[int, Path()],
        session: SessionDep
) -> GameClass:
    game_class = session.get(GameClass, class_id)

    if not game_class:
        raise HTTPException(404, "GameClass not found")

    return game_class


@game_classes_router.put(
    "/{class_id}",
    status_code=200,
    response_model=GameClass
)
async def replace_game_class(
        class_id: Annotated[int, Path()],
        game_class_base: GameClassBase,
        session: SessionDep
) -> GameClass:
    game_class = session.get(GameClass, class_id)

    if not game_class:
        raise HTTPException(404, "GameClass not found")

    new_data = game_class_base.model_dump()

    for key, value in new_data.items():
        setattr(game_class, key, value)

    session.add(game_class)
    session.commit()
    session.refresh(game_class)

    return game_class


@game_classes_router.delete(
    "/{class_id}",
    status_code=204
)
async def delete_game_class(
        class_id: Annotated[int, Path()],
        session: SessionDep
) -> None:
    game_class = session.get(GameClass, class_id)

    if not game_class:
        raise HTTPException(404, "GameClass not found")

    if game_class.players and len( game_class.players ) > 0:
        raise HTTPException(
            409,
            "Cannot delete GameClass: players are linked to this class"
        )

    session.delete(game_class)
    session.commit()
