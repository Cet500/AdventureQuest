from typing import Annotated

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models.effects import Effect, EffectBase
from api.db import SessionDep


effects_router = APIRouter()


@effects_router.post( '/effects' )
async def create_effect(
        effect_base: EffectBase,
        session: SessionDep
) -> dict:
    effect = Effect(
        name = effect_base.name,
        description = effect_base.description,
        duration = effect_base.duration,
        type = effect_base.type
    )
    effect.set_impact( effect_base.impact )

    session.add( effect )
    session.commit()
    session.refresh( effect )

    return { 'id': effect.id }


@effects_router.get( '/effects', response_model=list[Effect] )
async def get_effects(
        session: SessionDep
) -> dict:
    effects = session.exec( select(Effect) ).all()
    return effects


@effects_router.get( '/effects/{effect_id}' )
async def get_effect_by_id(
        effect_id: Annotated[ int, Path() ],
        session: SessionDep
) -> Effect:
    effect = session.get( Effect, effect_id )

    if not effect:
        raise HTTPException( 404, 'Effect not found' )

    return effect

