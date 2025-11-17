from typing import Annotated

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models.items import Item, ItemBase
from api.db import SessionDep


items_router = APIRouter()


@items_router.post( '/items' )
async def create_item(
		item_base: ItemBase,
		session: SessionDep
) -> dict:
	item = Item(
		name           = item_base.name,
        description    = item_base.description,
		weight         = item_base.weight,
		cost           = item_base.cost,
		rarity         = item_base.rarity,
		type           = item_base.type,
		attributes     = item_base.attributes,
	)

	session.add( item )
	session.commit()
	session.refresh( item )

	return { 'id': item.id }


@items_router.get( '/items',  response_model=list[Item] )
async def get_items(
		session: SessionDep
) -> dict:
	items = session.exec( select(Item) ).all()
	return items


@items_router.get( '/items/{item_id}' )
async def get_item_by_id(
	item_id: Annotated[ int, Path() ],
	session: SessionDep
) -> Item:
	item = session.get( Item, item_id )

	if not item:
		raise HTTPException( 404, 'Item not found' )

	return item