from typing import Annotated

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models.inventory import Inventory, InventoryBase
from api.db import SessionDep


inventory_router = APIRouter()


@inventory_router.post( '/inventory' )
async def create_inventory(
		inventory_base: InventoryBase,
		session: SessionDep
) -> dict:
	inventory = Inventory(
        player_id    = inventory_base.player_id,
        item_id      = inventory_base.item_id,
        quantity     = inventory_base.quantity,
        is_equipped  = inventory_base.is_equipped,
    )


	session.add( inventory )
	session.commit()
	session.refresh( inventory )

	return {'id': inventory.id}


@inventory_router.get( '/inventory',  response_model=list[Inventory] )
async def get_inventory(
		session: SessionDep
) -> dict:
	inventories = session.exec( select(Inventory) ).all()
	return inventories


@inventory_router.get( '/inventory/{inventory_id}' )
async def get_inventory_by_id(
	inventory_id: Annotated[ int, Path() ],
	session: SessionDep
) -> Inventory:
	inventory = session.get( Inventory, inventory_id )

	if not inventory:
		raise HTTPException( 404, 'Inventory not found' )

	return inventory

