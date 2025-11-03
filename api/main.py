from fastapi import FastAPI
from api.urls.users import users_router


app = FastAPI( version = '0.0.1' )

app.include_router( users_router )


@app.get('/')
async def home() -> dict:
    return { 'message': 'Hello world!' }
