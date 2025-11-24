from typing import Annotated, List

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models import User, UserBase
from api.models.users import UserID
from api.db import SessionDep
import logging


logger = logging.getLogger(__name__)
users_router = APIRouter( prefix = '/users', tags = [ 'users' ] )


@users_router.post(
	'',
	status_code = 201,
	response_model = UserID
)
async def create_user(
		user_base: UserBase,
		session: SessionDep
) -> UserID:
	existing_user = session.exec(
		select( User ).where( User.tg_id == user_base.tg_id )
	).first()

	if existing_user:
		raise HTTPException( 409, 'User already exists' )

	user = User.model_validate( user_base.model_dump() )

	session.add( user )
	session.commit()
	session.refresh( user )

	return UserID( id = user.id )


@users_router.get(
	'',
	status_code = 200,
	response_model = List[User]
)
async def get_users(
		session: SessionDep
) -> List[User]:
	users = session.exec( select(User) ).all()
	return users


@users_router.get(
	'/{user_id}',
	status_code = 200,
	response_model = User
)
async def get_user_by_id(
	user_id: Annotated[ int, Path() ],
	session: SessionDep
) -> User:
	user = session.get( User, user_id )

	if not user:
		raise HTTPException( 404, 'User not found' )

	return user


@users_router.get(
	'/tg/{tg_id}',
	status_code = 200,
	response_model = User
)
async def get_user_by_tg_id(
	tg_id:   Annotated[ int, Path() ],
	session: SessionDep
) -> User:
	user = session.exec( select( User ).where( User.tg_id == tg_id ) ).first()

	if not user:
		raise HTTPException( 404, 'User not found' )

	return user


@users_router.put(
	"/{user_id}",
	status_code = 200,
	response_model=User
)
async def replace_user(
	user_id: Annotated[int, Path()],
	user_base: UserBase,
	session: SessionDep
) -> User:
	user = session.get(User, user_id)

	if not user:
		raise HTTPException(404, "User not found")

	new_data = user_base.model_dump()

	for key, value in new_data.items():
		setattr(user, key, value)

	session.add(user)
	session.commit()
	session.refresh(user)

	return user


@users_router.delete(
	"/{user_id}",
	status_code=204
)
async def delete_user(
	user_id: Annotated[ int, Path() ],
	session: SessionDep
) -> None:
	user = session.get(User, user_id)

	if not user:
		raise HTTPException(404, "User not found")

	session.delete(user)
	session.commit()
