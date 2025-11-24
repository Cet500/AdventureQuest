from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class InventoryBase( SQLModel ):
    player_id: int    = Field( foreign_key="player.id", nullable=False )
    item_id: int      = Field( foreign_key="item.id", nullable=False )
    quantity: int     = Field( default = 0 )
    is_equipped: bool = Field( default = False )


class Inventory( InventoryBase, table = True ):
    id:     int | None         = Field( default = None, primary_key = True )
    player: Optional["Player"] = Relationship()
    item:   Optional["Item"]   = Relationship()


class InventoryID( SQLModel ):
    id: int
