from typing import Annotated

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models import User, UserBase
from api.db import SessionDep


users_router = APIRouter()


@users_router.post('/users')
async def create_user(
		user_base: UserBase,
		session: SessionDep
) -> dict:
	user = User(
		tg_id = user_base.tg_id,
		name  = user_base.name,
		lang  = user_base.lang,
		email = user_base.email,
		phone = user_base.phone
	)

	session.add( user )
	session.commit()
	session.refresh( user )

	return { 'id': user.id }


@users_router.get( '/users',  response_model=list[User] )
async def get_users(
		session: SessionDep
) -> dict:
	users = session.exec( select(User) ).all()
	return users


@users_router.get( '/users/{user_id}' )
async def get_user_by_id(
	user_id: Annotated[ int, Path() ],
	session: SessionDep
) -> User:
	user = session.get( User, user_id )

	if not user:
		raise HTTPException( 404, 'User not found' )

	return user
