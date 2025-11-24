from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from pydantic import EmailStr, field_validator, model_validator
import phonenumbers


class Verify(str, Enum):
    N = 'None verified'
    A = 'Auto checked',
    V = 'Verified'
    R = 'Real checked'


class UserBase( SQLModel ):
    tg_id        : int
    name         : str             = Field( max_length = 40 )
    lang         : str | None      = 'ru'

    email        : EmailStr | None = Field( default = None, max_length = 100 )
    verify_email : Verify          = Verify.N

    phone        : str | None      = Field( default = None, max_length = 20 )
    verify_phone : Verify          = Verify.N

    @field_validator( 'phone', mode = 'before' )
    @classmethod
    def validate_phone( cls, v ):
        if v is None or v == "":
            return None

        try:
            parsed = phonenumbers.parse( v, None )

            if not phonenumbers.is_valid_number( parsed ):
                raise ValueError( "Invalid phone number" )

            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )

        except phonenumbers.NumberParseException:
            raise ValueError( "Invalid phone number format" )

    @model_validator( mode = 'after' )
    def set_auto_verified( self ):
        if self.phone and self.verify_phone == Verify.N:
            self.verify_phone = Verify.A

        if self.email and self.verify_email == Verify.N:
            self.verify_email = Verify.A

        return self


class User( UserBase, table = True ):
    __tablename__ = "user"

    id     : int | None         = Field( default = None, primary_key = True )

    player : Optional["Player"] = Relationship(
        back_populates = "user",
        sa_relationship_kwargs={"uselist": False}
    )

    datetime_reg: datetime = Field(
        default_factory = lambda: datetime.now( timezone.utc ),
        sa_column = Column( DateTime( timezone = True ), server_default = func.now() )
    )
    datetime_upd: datetime = Field(
        default_factory = lambda: datetime.now( timezone.utc) ,
        sa_column = Column( DateTime( timezone = True ), onupdate = func.now(), server_default = func.now() )
    )



class UserID( SQLModel ):
    id: int
