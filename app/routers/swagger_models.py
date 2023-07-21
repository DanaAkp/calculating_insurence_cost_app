import uuid
import datetime
from typing import List, Dict, Union

from pydantic import BaseModel, Field, validator


class DataBaseModel(BaseModel):
    class Config:
        orm_mode = True


class TariffPlanDataIN(DataBaseModel):
    date: datetime.date
    cargo_type_name: str
    rate: float


class Tariff(DataBaseModel):
    cargo_type: str
    rate: float


class JSONTariffPlansDataIN(DataBaseModel):
    data: Dict[datetime.date, List[Tariff]] = Field(default={
        '2020-07-26': [
            {
                'cargo_type': 'other',
                'rate': 0.3
            },
            {
                'cargo_type': 'glass',
                'rate': 0.1
            }
        ]
    })


class EditTariffPlanDataIN(DataBaseModel):
    cargo_type_id: Union[str, uuid.UUID]
    rate: float

    @validator('cargo_type_id')
    def validate_cargo_type_id(cls, value):
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class TariffPlanData(DataBaseModel):
    id: uuid.UUID
    date: datetime.date
    cargo_type_id: uuid.UUID
    rate: float

    @validator('cargo_type_id')
    def validate_cargo_type_id(cls, value):
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class CargoTypeData(DataBaseModel):
    id: uuid.UUID
    name: str


class CalculatingDataIn(DataBaseModel):
    declared_value: float
    cargo_type_id: str


class CalculatingData(DataBaseModel):
    insurance_cost: float
