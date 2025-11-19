from sqlmodel import SQLModel, Field


class UserBase( SQLModel ):
    tg_id: int
    name: str
    lang: str | None = Field( default = 'ru' )
    email: str | None
    phone: str | None


class User( UserBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )
