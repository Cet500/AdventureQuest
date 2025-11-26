from typing import Dict, Any

from sqlmodel import SQLModel, Field
from enum import Enum
from sqlalchemy import Column, String
from api.types.json import JsonType


class Rarities(str, Enum):
    common    = 'Обычный"'
    uncommon  = 'Необычный'
    rare      = 'Редкий'
    epic      = 'Эпический'
    legendary = 'Легендарный'
    mythical  = 'Мифический'
    secret    = 'Секретный'


class Types(str, Enum):
    weapon     = 'Оружие'
    shield     = 'Щит'
    armor      = 'Броня'
    consumable = 'Расходуемое'


class ItemBase( SQLModel ):
    name        : str = Field( max_length = 40 )
    description : str = Field( max_length = 250 )
    symbol      : str = Field( max_length = 1 )

    weight      : int      = 0
    cost        : int      = 0
    rarity      : Rarities = Rarities.common
    type        : Types

    attributes  : Dict[str, Any] = Field(
        default_factory = dict,
        sa_column = Column( JsonType, nullable = False )
    )


class Item( ItemBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )
    image       : str | None = Field(
        default = None,
        description = "Путь к изображению относительно media/"
    )

class ItemID( SQLModel ):
    id: int


