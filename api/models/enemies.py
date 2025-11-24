from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Dict, Any
from sqlalchemy import Column, String


class EnemyBase( SQLModel ):
    name: str
    loot: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(String, nullable=False))
    desсription: str
    reward_xp: int      = Field( default= 10 )
    hp: int             = Field( default = 100 )
    mp: int             = Field( default = 0 )
    max_hp: int         = Field( default = 0 )
    damage: int         = Field( default = 0 )
    armor: int          = Field( default = 0 )
    max_armor: int      = Field( default = 0 )
    level: int          = Field( default = 0 )
    reward_money: int   = Field( default = 10 )


class Enemy( EnemyBase, table = True ):
    __tablename__ = 'enemy'

    id: int | None = Field( default = None, primary_key = True )
