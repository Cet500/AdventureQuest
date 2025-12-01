from typing import Any, Dict

from sqlalchemy import Column
from sqlmodel import Relationship, SQLModel, Field

from api.types.json import JsonType


class LocationBase( SQLModel ):
    name        : str = Field( max_length = 128 )
    description : str

    image : str | None = Field(
        default = None,
        description = "Путь к изображению относительно media/"
    )

    image_width  : int | None = None
    image_height : int | None = None
    image_size   : int | None = None  # bytes
    image_mime   : str | None = Field( default = None, max_length = 64 )


class Location( LocationBase, table = True ):
    id : int | None = Field( default = None, primary_key = True )

    exits: list["LocationTransition"] = Relationship(
        back_populates = "from_location",
        sa_relationship_kwargs = { "foreign_keys": "LocationTransition.from_location_id" },
    )
    entries: list["LocationTransition"] = Relationship(
        back_populates = "to_location",
        sa_relationship_kwargs = { "foreign_keys": "LocationTransition.to_location_id" },
    )

class LocationID( SQLModel ):
    id : int


class LocationURL( SQLModel ):
    url : str


class LocationTransitionBase( SQLModel ):
    title       : str        = Field( max_length = 64 )  # куда
    description : str | None = Field( default = None, max_length = 250 )  # процесс перехода

    condition   : Dict[str, Any] = Field(
        default_factory = dict,
        sa_column = Column( JsonType, nullable = False )
    )


class LocationTransition( LocationTransitionBase, table = True ):
    from_location_id: int = Field(
        foreign_key = "location.id", primary_key = True
    )
    to_location_id: int = Field(
        foreign_key = "location.id", primary_key = True
    )

    from_location: Location = Relationship(
        back_populates = "exits",
        sa_relationship_kwargs = { "foreign_keys": "LocationTransition.from_location_id" },
    )
    to_location: Location = Relationship(
        back_populates = "entries",
        sa_relationship_kwargs = { "foreign_keys": "LocationTransition.to_location_id" },
    )


class LocationTransitionCreate( SQLModel ):
    from_location_id : int
    to_location_id   : int
    title            : str
    description      : str | None = None
    condition        : str | None = None


class LocationTransitionRead( SQLModel ):
    from_location_id : int
    to_location_id   : int
    title            : str
    description      : str | None = None
    condition        : str | None = None
