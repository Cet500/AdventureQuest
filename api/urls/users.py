from typing import Annotated
from fastapi import Path, APIRouter

from api.db import users


users_router = APIRouter()


@users_router.get('/users')
async def get_users() -> dict:
    return users

@users_router.post('/user/{login}/{hp}/{damage}/{armor}')
async def post_user(
        login : Annotated[ str, Path() ] ,
        hp    : Annotated[ int, Path( gt=0, le=100 ) ],
        damage: Annotated[ int, Path( gt=0, le=100 ) ],
        armor : Annotated[ int, Path( gt=0, le=100 ) ],
) -> dict:
    users[login] = {
        'hp': hp,
        'damage': damage,
        'armor': armor
    }

    return users[login]