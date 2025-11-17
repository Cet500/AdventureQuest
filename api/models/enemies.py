from sqlmodel import SQLModel, Field


class EnemyBase( SQLModel ):
    names: str
    hp: int          = Field( default = 100 )
    mp: int          = Field( default = 0 )
    max_hp: int      = Field( default = 0 )
    damage: int      = Field( default = 0 )
    armor: int       = Field( default = 0 )
    max_armor: int   = Field( default = 0 )
    level: int       = Field( default = 0 )
    money: int       = Field( default = 10 )

class Enemy( EnemyBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )
