from typing import Dict, Any, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from api.types.json import JsonType


class GameClassBase( SQLModel ):
    symbol      : str = Field( max_length = 1 )
    name        : str = Field( max_length = 20 )
    description : str = Field( max_length = 200 )

    delta_attributes : Dict[str, Any] = Field(
        default_factory = dict,
        sa_column = Column( JsonType, nullable = False )
    )


class GameClass( GameClassBase, table = True ):
    __tablename__ = "game_class"

    id: int | None = Field(default=None, primary_key=True)

    players: List["Player"] = Relationship(back_populates="game_class" )


class GameClassID( SQLModel ):
    id: int
