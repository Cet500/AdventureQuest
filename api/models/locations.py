from sqlmodel import SQLModel, Field


class LocationBase( SQLModel ):
    name: str
    description: str
    image: str


class Location( LocationBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )