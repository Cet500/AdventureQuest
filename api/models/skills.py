# from typing import Dict, Any, Optional
#
# from sqlmodel import SQLModel, Field, Relationship
# from sqlalchemy import Column, String
#
#
# class SkillClassLink(SQLModel, table=True):
#     __tablename__ = "skill_class_link"
#
#     skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
#     class_id: Optional[int] = Field(default=None, foreign_key="game_class.id", primary_key=True)
#
#
# class SkillBase( SQLModel ):
#     name: str
#     description: str
#     required_level: int
#     cooldown: int
#     attributes: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(String, nullable=False))
#
#
# class Skill( SkillBase, table = True ):
#     id:      int | None = Field(default=None, primary_key=True)
#     classes: list["GameClass"] = Relationship(back_populates="skills", link_model=SkillClassLink)
