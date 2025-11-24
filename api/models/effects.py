import json
from enum import Enum
from typing import Dict, Any

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String


class Types(str, Enum):
    positive = 'Положительный'
    negative = 'Негативный'
    neutral = 'Нейтральный'


class EffectBase( SQLModel ):
    name: str
    description: str
    duration: int
    type: Types
    impact: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(String, nullable=False))

    @classmethod
    def validate_impact(cls, impact: Dict[str, Any]) -> str:
        return json.dumps(impact, ensure_ascii=False)

    def set_impact(self, data: Dict[str, Any]):
        self.impact = json.dumps(data, ensure_ascii=False)

    def get_impact(self) -> Dict[str, Any]:
        return json.loads(self.impact)


class Effect( EffectBase, table = True ):
    __tablename__ = 'effect'

    id: int | None = Field( default = None, primary_key  = True)


class EffectID( SQLModel ):
    id: int
