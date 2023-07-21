import json
from datetime import datetime
from typing import List

from fastapi import HTTPException
from tortoise.expressions import Q

from app.models import TariffPlan
from app.models.cargo_type import CargoType
from app.controllers.cache import service


class TransfersService:
    KEY_ACTIVE_TARIFF = 'active_tariff_plans'
    KEY_CARGO_TYPES = 'active_cargo_types'
    DATE_FORMAT = "%Y-%B-%d"

    async def calculating_insurance(self, declared_value: float, cargo_type_id: str) -> dict:
        tariffs = await self.get_current_tariff_plans()
        for i in tariffs:
            if i.get('cargo_type_id') == cargo_type_id:
                rate = i.get('rate')
                break
        else:
            raise HTTPException(404, f'Not found tariff plan by cargo type with id {cargo_type_id}.')
        result = rate * declared_value
        return {'insurance_cost': result}

    async def get_all_cargo_type(self) -> List[dict]:
        if not (cargo_types_list := await service.get(self.KEY_CARGO_TYPES)):
            cargo_types_list = await self.set_current_cargo_types()
        return cargo_types_list

    async def get_current_tariff_plans(self) -> dict:
        if not (tariff_list := await service.get(self.KEY_ACTIVE_TARIFF)):
            tariff_list = await self.set_current_tariff_plans()
        return tariff_list

    async def set_current_tariff_plans(self) -> list:
        now = datetime.now().date()
        tariff = await TariffPlan.filter(Q(date__lte=now)).order_by('-date').all()
        tariff_list = []
        for t in tariff:
            tariff_list.append(
                dict(date=t.date.strftime(self.DATE_FORMAT), cargo_type_id=str(t.cargo_type_id), rate=t.rate)
            )
        await service.set(self.KEY_ACTIVE_TARIFF, tariff_list)
        return tariff_list

    async def set_current_cargo_types(self) -> list:
        current = datetime.strptime((await self.get_current_tariff_plans())[0].get('date'), self.DATE_FORMAT)
        cargo_types = await CargoType.filter(tariff_plans__date=current).distinct().all()
        cargo_types_list = []
        for c_t in cargo_types:
            cargo_types_list.append(dict(id=str(c_t.id), name=c_t.name))
        await service.set(self.KEY_CARGO_TYPES, cargo_types_list)
        return cargo_types_list
