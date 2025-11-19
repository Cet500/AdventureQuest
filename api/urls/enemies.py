from fastapi import APIRouter
from sqlmodel import select

from api.db import SessionDep
from api.models.enemies import Enemy, EnemyBase

enemies_router = APIRouter()


@enemies_router.post( '/enemies' )
async def create_enemies(
        enemies_base: EnemyBase,
        session: SessionDep
) -> dict:
    enemy = Enemy(
        name          = enemies_base.name,
        description   = enemies_base.desсription,
        loot          = enemies_base.loot,
        reward_xp     = enemies_base.reward_xp,
        hp            = enemies_base.hp,
        mp            = enemies_base.mp,
        max_hp        = enemies_base.max_hp,
        damage        = enemies_base.damage,
        armor         = enemies_base.armor,
        max_armor     = enemies_base.max_armor,
        level         = enemies_base.level,
        reward_money  = enemies_base.reward_money,
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

