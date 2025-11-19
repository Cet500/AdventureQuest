from fastapi import Path, APIRouter, HTTPException
from sqlmodel import select
from api.models.locations import Location, LocationBase
from api.db import SessionDep


location_router = APIRouter()


@location_router.post( '/locations' )
async def create_location(
        location_base: LocationBase,
        session: SessionDep
) -> dict:
    location = Location(
        name        = location_base.name,
        description = location_base.description,
        image       = location_base.image
    )

    session.add( location )
    session.commit()
    session.refresh( location )

    return { 'id': location.id }


@location_router.get( '/locations',  response_model=list[Location] )
async def get_locations(
        session: SessionDep
)  -> dict:
    locations = session.exec( select(Location) ).all()
    return locations
