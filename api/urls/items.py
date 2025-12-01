from typing import Annotated, List

from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models import Item, ItemBase
from api.models.items import ItemID
from api.db import SessionDep
import logging


logger = logging.getLogger(__name__)
items_router = APIRouter( prefix = '/items', tags = [ 'items' ] )


@items_router.post(
	'',
	status_code = 201
)
async def create_item(
		item_base: ItemBase,
		session: SessionDep
) -> ItemID:
	item = Item.model_validate( item_base.model_dump() )

	session.add( item )
	session.commit()
	session.refresh( item )

	return ItemID( id = item.id )


@items_router.get(
	'',
	status_code = 200,
	response_model=List[Item]
)
async def get_items(
		session: SessionDep
) -> List[Item]:
	items = session.exec( select(Item) ).all()
	return items


@items_router.get(
	'/{item_id}',
	status_code = 200,
	response_model = Item
)
async def get_item_by_id(
	item_id: Annotated[ int, Path() ],
	session: SessionDep
) -> Item:
	item = session.get( Item, item_id )

	if not item:
		raise HTTPException( 404, 'Item not found' )

	return item


@items_router.put(
	"/{item_id}",
	status_code = 200,
	response_model=Item
)
async def replace_item(
	item_id: Annotated[ int, Path() ],
	item_base: ItemBase,
	session: SessionDep
) -> Item:
	item = session.get(item_id)

	if not item:
		raise HTTPException(404, "Item not found")

	new_data = item_base.model_dump()

	for key, value in new_data.items():
		setattr(item, key, value)

	session.add(item)
	session.commit()
	session.refresh(item)

	return item


@items_router.delete(
	"/{item_id}",
	status_code=204
)
async def delete_item(
	item_id: Annotated[ int, Path() ],
	session: SessionDep
) -> None:
	item = session.get(Item, item_id)

	if not item:
		raise HTTPException(404, "Item not found")

	session.delete(item)
	session.commit()
