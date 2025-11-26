from sqlmodel import SQLModel, Field


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


class LocationID( SQLModel ):
    id : int


class LocationURL( SQLModel ):
    url : str
