from typing import Dict, Any

from sqlmodel import SQLModel, Field
from enum import Enum
from sqlalchemy import Column, String


class Rarities(str, Enum):
    common    = 'Обычный"'
    uncommon  = 'Необычный'
    rare      = 'Редкий'
    epic      = 'Эпичический'
    legendary = 'Легендарный'
    mythical  = 'Мифический'
    secret    = 'Секретный'


class Types(str, Enum):
    weapon     = 'Оружие'
    shield     = 'Щит'
    armor      = 'Броня'
    consumable = 'Расходуемое'


class ItemBase( SQLModel ):
    name: str
    description: str
    weight: int  = Field( default = 0 )
    cost: int    = Field( default = 0 )
    rarity: Rarities
    type: Types
    attributes: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(String, nullable=False))


class Item( ItemBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )


class ItemID( SQLModel ):
    id: int
