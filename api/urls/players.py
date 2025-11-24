from typing import Annotated, List

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models import Player, PlayerBase, User
from api.models.players import PlayerID
from api.db import SessionDep
import logging


logger = logging.getLogger(__name__)
players_router = APIRouter( prefix = '/players', tags = [ 'players' ] )


@players_router.post(
	'',
	status_code = 201
)
async def create_player(
		player_base: PlayerBase,
		session: SessionDep
) -> PlayerID:
	user = session.get( User, player_base.user_id )

	if not user:
		raise HTTPException( 404, "User not found" )

	if user.player is not None:
		raise HTTPException( 409, "Player for this user already exists" )

	player = Player.model_validate( player_base.model_dump() )

	session.add( player )
	session.commit()
	session.refresh( player )

	return PlayerID( id = player.id )


@players_router.get(
	'',
	status_code = 200,
	response_model=list[Player]
)
async def get_players(
		session: SessionDep
) -> List[Player]:
	players = session.exec( select(Player) ).all()
	return players


@players_router.get(
	'/{player_id}',
	status_code = 200,
	response_model = Player
)
async def get_player_by_id(
	player_id: Annotated[ int, Path() ],
	session: SessionDep
) -> Player:
	player = session.get( Player, player_id )

	if not player:
		raise HTTPException( 404, 'Player not found' )

	return player


@players_router.get(
	"/user/{user_id}",
	status_code = 200,
	response_model=Player
)
async def get_player_by_user_id(
	user_id: Annotated[ int, Path() ],
	session: SessionDep
):
	user = session.get(User, user_id)

	if not user:
		raise HTTPException(404, "User not found")

	if not user.player:
		raise HTTPException(404, "Player not found")

	return user.player


@players_router.get(
	"/tg/{tg_id}",
	status_code = 200,
	response_model=Player
)
async def get_player_by_user_tg_id(
	tg_id: Annotated[ int, Path() ],
	session: SessionDep
):
	user = session.exec( select( User ).where( User.tg_id == tg_id ) ).first()

	if not user:
		raise HTTPException(404, "User not found")

	if not user.player:
		raise HTTPException(404, "Player not found")

	return user.player


@players_router.put(
	"/{player_id}",
	status_code = 200,
	response_model=Player
)
async def replace_player(
	player_id: Annotated[ int, Path() ],
	player_base: PlayerBase,
	session: SessionDep
) -> Player:
	player = session.get(User, player_id)

	if not player:
		raise HTTPException(404, "Player not found")

	new_data = player_base.model_dump()

	for key, value in new_data.items():
		setattr(player, key, value)

	session.add(player)
	session.commit()
	session.refresh(player)

	return player


@players_router.delete(
	"/{player_id}",
	status_code=204
)
async def delete_player(
	player_id: Annotated[ int, Path() ],
	session: SessionDep
) -> None:
	player = session.get(User, player_id)

	if not player:
		raise HTTPException(404, "Player not found")

	session.delete(player)
	session.commit()
