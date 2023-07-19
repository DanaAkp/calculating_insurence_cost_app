import logging
import datetime
import traceback
import uuid
from typing import List, Union

import tortoise.transactions
from fastapi import HTTPException

from app.config import SECRET
from app.models.tariff_plan import TariffPlan
from app.models.cargo_type import CargoType
from app.controllers import transfers_service

log = logging.getLogger('api_log')


class TariffPlanService:
    async def create_tariff_plan(self, date: datetime.date, cargo_type: str, rate: float) -> TariffPlan:
        try:
            if result := await self._create_tariff_plan_in_db(date, cargo_type, rate):
                return result
        except Exception as error:
            log.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, 'Failed to create a new tariff plan.')
        raise HTTPException(400, 'Such a tariff plan already exists. Try updating it.')

    async def get_cargo_type_by_name(self, cargo_type: str) -> CargoType:
        return (await CargoType.get_or_create(name=cargo_type))[0]

    @tortoise.transactions.atomic()
    async def _create_tariff_plan_in_db(self, date: datetime.date, cargo_type_name: str, rate: float) -> TariffPlan:
        cargo_type = await self.get_cargo_type_by_name(cargo_type_name)
        tariff = await TariffPlan.filter(
            date=date,
            cargo_type_id=cargo_type.id
        ).get_or_none()
        if not tariff:
            tariff = TariffPlan(date=date, cargo_type_id=cargo_type.id, rate=rate)
            await tariff.save()
            return tariff

    async def get_all_tariff_plans(self) -> Union[List[TariffPlan], TariffPlan]:
        return await TariffPlan.all()

    async def update_tariff_plan(self, tariff_plan_id: uuid.UUID, cargo_type_id: uuid.UUID, rate: float) -> TariffPlan:
        try:
            if result := await self._update_tariff_plan_in_db(tariff_plan_id, cargo_type_id, rate):
                return result
        except Exception as error:
            log.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, f'Failed to update tariff plan by id {tariff_plan_id}.')
        raise HTTPException(404, f'Not found tariff plan by id {tariff_plan_id}.')

    @tortoise.transactions.atomic()
    async def _update_tariff_plan_in_db(self, tariff_plan_id: uuid.UUID, cargo_type_id: uuid.UUID,
                                        rate: float) -> TariffPlan:
        tariff = await TariffPlan.filter(id=tariff_plan_id).get_or_none()
        if tariff:
            tariff.rate = rate
            tariff.cargo_type_id = cargo_type_id
            await TariffPlan.bulk_update(objects=(tariff,), fields=('rate', 'cargo_type_id'))
            return tariff

    async def delete_tariff_plane(self, tariff_id: str) -> dict:
        tariff = await TariffPlan.get(id=uuid.UUID(tariff_id))
        current = await transfers_service.get_current_tariff_plan()
        if current.date == tariff.date:
            raise HTTPException(403, f'Forbidden to delete current tariff plan.')

        try:
            await tariff.delete()
        except Exception as error:
            log.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, f'Failed to delete tariff plan by id {tariff_id}')
        else:
            return {'success': True}

    @tortoise.transactions.atomic()
    async def _upload_from_dict_to_db(self, data: dict) -> None:
        for k, tariffs in data.items():
            for tariff in tariffs:
                cargo_type = await self.get_cargo_type_by_name(tariff.cargo_type)
                tariff_plan = TariffPlan(date=k, cargo_type_id=cargo_type.id, rate=tariff.rate)
                await tariff_plan.save()

    async def upload_from_dict(self, data: dict) -> dict:
        try:
            await self._upload_from_dict_to_db(data)
        except Exception as error:
            log.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, 'Failed to upload tariff plans.')
        return {'success': True}

    async def is_valid_token(self, token: str) -> bool:
        if token == SECRET:
            return True
        return False
