import uuid
from datetime import datetime
from typing import List

from tortoise.expressions import Q

from app.models import TariffPlan
from app.models.cargo_type import CargoType


class TransfersService:

    async def get_current_tariff_by_cargo_type(self, cargo_type_id: uuid.UUID) -> TariffPlan:
        now = datetime.now().date()

        tariff = await TariffPlan \
            .filter(Q(date__lte=now)) \
            .filter(cargo_type_id=cargo_type_id) \
            .order_by('-date') \
            .first()
        return tariff

    async def calculating_insurance(self, declared_value: float, cargo_type_id: uuid.UUID) -> dict:
        current = await self.get_current_tariff_by_cargo_type(cargo_type_id)
        result = current.rate * declared_value
        return {'insurance_cost': result}

    async def get_all_cargo_type(self) -> List[CargoType]:
        current = await TariffPlan \
            .filter(Q(date__lte=datetime.now().date())) \
            .order_by('-date').first()
        cargo_types = await CargoType.filter(tariff_plans__date=current.date).distinct().all()
        return cargo_types
