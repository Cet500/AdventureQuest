from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from api.models.game_classes import GameClass


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

    game_class_id: Optional[int] = Field(
        default=None,
        foreign_key="gameclass.id"
    )


class Player( PlayerBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )
    game_class: Optional["GameClass"] = Relationship(back_populates="players")


class PlayerID( SQLModel ):
    id: int
