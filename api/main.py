from fastapi import FastAPI
from api.urls.users import users_router
from api.config import VERSION


app = FastAPI( version = VERSION )

app.include_router( users_router )


@app.get('/')
async def home() -> dict:
    return { 'message': 'Hello world 2222!' }
