from typing import Annotated

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models.players import Player, PlayerBase
from api.db import SessionDep


players_router = APIRouter()


@players_router.post( '/players' )
async def create_player(
		player_base: PlayerBase,
		session: SessionDep
) -> dict:
	player = Player(
		nickname  = player_base.nickname,
		hp        = player_base.hp,
		max_hp    = player_base.max_hp,
		mp        = player_base.mp,
		max_mp    = player_base.max_mp,
		damage    = player_base.damage,
		armor     = player_base.armor,
		max_armor = player_base.max_armor,
		xp        = player_base.xp,
		level     = player_base.level,
		money     = player_base.money,
	)

	session.add( player )
	session.commit()
	session.refresh( player )

	return { 'id': player.id }


@players_router.get( '/players',  response_model=list[Player] )
async def get_players(
		session: SessionDep
) -> dict:
	players = session.exec( select(Player) ).all()
	return players


@players_router.get( '/players/{player_id}' )
async def get_player_by_id(
	player_id: Annotated[ int, Path() ],
	session: SessionDep
) -> Player:
	player = session.get( Player, player_id )

	if not player:
		raise HTTPException( 404, 'Player not found' )

	return player