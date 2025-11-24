from typing import Annotated, List

from fastapi import Path, APIRouter, HTTPException, UploadFile, Form, Request
from sqlmodel import select

from api.models.locations import Location, LocationID, LocationURL
from api.db import SessionDep
from api.utils.images import validate_and_save_image


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
		rel_path, w, h, size, mime = validate_and_save_image( image )
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
