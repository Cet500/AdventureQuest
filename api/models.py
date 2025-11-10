from sqlmodel import SQLModel, Field


class PlayerBase( SQLModel ):
    nickname: str

class Player( PlayerBase, table = True ):
    id: int | None = Field( default = None, primary_key = True )

class PlayerID( SQLModel ):
    id: int
