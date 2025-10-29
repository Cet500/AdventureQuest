from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI( version = '0.0.1' )

users = {}

@app.get('/users/')
async def get_users() -> dict:
    return users

@app.post('/user/{login}/{hp}/{damage}/{armor}')
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
