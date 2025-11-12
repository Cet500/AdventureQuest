from sqlmodel import SQLModel, Field


class UserBase( SQLModel ):
    tg_id: int
    name: str
    lang: str | None = Field( default = 'ru' )
    email: str | None
    phone: str | None

class User( UserBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )


class PlayerBase( SQLModel ):
    nickname: str
    hp: int        = Field( default = 100 )
    max_hp: int    = Field( default = 100 )
    mp: int        = Field( default = 0 )
    max_mp: int    = Field( default = 0 )
    damage: int    = Field( default = 0 )
    armor: int     = Field( default = 0 )
    max_armor: int = Field( default = 0 )
    xp: int        = Field( default = 0 )
    level: int     = Field( default = 0 )
    money: int     = Field( default = -100 )

class Player( PlayerBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )

class PlayerID( SQLModel ):
    id: int
