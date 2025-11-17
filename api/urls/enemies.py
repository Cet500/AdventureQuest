from typing import Annotated

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models.enemies import Enemy, EnemyBase
from api.db import SessionDep


enemies_router = APIRouter()


@enemies_router.post( '/enemies' )
async def create_enemies(
        enemies_base: EnemyBase,
        session: SessionDep
) -> dict:
    enemy = Enemy(
        names     = enemies_base.names,
        hp        = enemies_base.hp,
        mp        = enemies_base.mp,
        max_hp    = enemies_base.max_hp,
        damage    = enemies_base.damage,
        armor     = enemies_base.armor,
        max_armor = enemies_base.max_armor,
        level     = enemies_base.level,
        money     = enemies_base.money,
    )

    session.add( enemy )
    session.commit()
    session.refresh( enemy )

    return { 'id': enemy.id }


@enemies_router.get( '/enemies',  response_model=list[Enemy] )
async def get_enemies(
        session: SessionDep
)  -> dict:
    enemies = session.exec( select(Enemy) ).all()
    return enemies

