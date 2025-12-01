from typing import Annotated, List

from fastapi import Path, APIRouter, HTTPException, UploadFile, Form, Request, Body
from sqlmodel import select

from api.models import Location, LocationTransition
from api.models.locations import (LocationID, LocationURL,
                                  LocationTransitionRead, LocationTransitionCreate)
from api.db import SessionDep
from api.utils.images import validate_and_save_image
from ..config import LOCATION_FOLDER

location_router = APIRouter( prefix = "/locations", tags = [ "locations" ] )


@location_router.post(
	'/locations',
	status_code = 201,
	response_model = LocationID
)
async def create_location(
		session: SessionDep,
		name: str = Form(...),
		description: str = Form(...),
		image: UploadFile | None = None
) -> LocationID:
	if image:
		rel_path, w, h, size, mime = validate_and_save_image( image, LOCATION_FOLDER )
	else:
		raise HTTPException( 400, "Image is required" )

	location = Location(
		name         = name,
		description  = description,
		image        = rel_path,
		image_width  = w,
		image_height = h,
		image_size   = size,
		image_mime   = mime
	)

	session.add( location )
	session.commit()
	session.refresh( location )

	return LocationID( id = location.id )


@location_router.get(
	'/locations',
	status_code = 200,
	response_model = List[Location]
)
async def get_locations(
		session: SessionDep
)  -> List[Location]:
	locations = session.exec( select(Location) ).all()
	return locations


@location_router.get(
	'/{location_id}',
	status_code = 200,
	response_model = Location
)
async def get_location_by_id(
	location_id: Annotated[ int, Path() ],
	session: SessionDep
) -> Location:
	location = session.get( Location, location_id )

	if not location:
		raise HTTPException( 404, 'Location not found' )

	return location


@location_router.get(
	'/{location_id}/url',
	status_code = 200,
	response_model = LocationURL
)
async def get_location_full_url_by_id(
	location_id: Annotated[ int, Path() ],
	session: SessionDep,
	request: Request = None
) -> LocationURL:
	location = session.get( Location, location_id )

	if not location:
		raise HTTPException( 404, 'Location not found' )


	full_url = request.url_for( "static", path = location.image )

	return LocationURL( url = str( full_url ) )


@location_router.delete(
	"/{location_id}",
	status_code=204
)
async def delete_location(
		location_id: Annotated[int, Path()],
		session: SessionDep
) -> None:
	location = session.get(Location, location_id)

	if not location:
		raise HTTPException( 404, "Location not found")

	session.delete(location)
	session.commit()


@location_router.post(
	"/transitions",
	status_code=201,
	response_model=LocationTransitionRead,
)
async def create_location_transition(
	transition_data: LocationTransitionCreate = Body(...),
	session: SessionDep = None,
) -> LocationTransition:
	from_location = session.get(Location, transition_data.from_location_id)
	to_location = session.get(Location, transition_data.to_location_id)

	if not from_location or not to_location:
		raise HTTPException(404, "One or both locations not found")

	transition = LocationTransition(
		from_location_id=transition_data.from_location_id,
		to_location_id=transition_data.to_location_id,
		title=transition_data.title,
		direction=transition_data.direction,
		condition=transition_data.condition,
	)

	session.add(transition)
	session.commit()
	session.refresh(transition)

	return transition


@location_router.get(
	"/{location_id}/transitions",
	status_code=200,
	response_model=List[LocationTransitionRead],
)
async def get_location_transitions(
	location_id: int,
	session: SessionDep,
) -> List[LocationTransitionRead]:
	statement = select(LocationTransition).where(LocationTransition.from_location_id == location_id)
	results = session.exec(statement).all()
	return results


@location_router.delete(
	"/transitions",
	status_code=204,
)
async def delete_location_transition(
	from_location_id: int,
	to_location_id: int,
	session: SessionDep,
):
	transition = session.get(LocationTransition, (from_location_id, to_location_id))

	if not transition:
		raise HTTPException(404, "Transition not found")

	session.delete(transition)
	session.commit()
