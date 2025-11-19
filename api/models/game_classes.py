from typing import Dict, Any

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from api.models.players import Player
from api.models.skills import Skill, SkillClassLink


class GameClassBase( SQLModel ):
    name: str
    description: str
    delta_attributes: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(String, nullable=False))


class GameClass( GameClassBase, table = True ):
    id: int | None = Field(default=None, primary_key=True)
    players: list["Player"] = Relationship(back_populates="game_class")
    skills:  list["Skill"] = Relationship(back_populates="classes", link_model=SkillClassLink)