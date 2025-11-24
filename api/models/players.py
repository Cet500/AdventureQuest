from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class PlayerBase( SQLModel ):
    nickname      : str = Field(
        min_length = 2,
        max_length = 64
    )
    user_id       : int = Field(
        foreign_key = "user.id",
        unique = True,
        index = True
    )
    game_class_id : int = Field(
        default = None,
        foreign_key = "game_class.id"
    )

    hp         : int = 100
    max_hp     : int = 100
    mp         : int = 0
    max_mp     : int = 0
    damage     : int = 0
    armor      : int = 0
    max_armor  : int = 0
    xp         : int = 0
    level      : int = 0
    weight     : int = 0
    weight_max : int = 0
    money      : int = -100


class Player( PlayerBase, table = True ):
    __tablename__ = "player"

    id: int | None = Field( default = None, primary_key = True )

    user:       Optional["User"]      = Relationship( back_populates = "player" )
    game_class: Optional["GameClass"] = Relationship( back_populates = "players" )


class PlayerID( SQLModel ):
    id: int
