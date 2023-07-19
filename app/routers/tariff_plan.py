import uuid
from typing import List

from fastapi import APIRouter, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.routers.swagger_models import TariffPlanData, TariffPlanDataIN, EditTariffPlanDataIN, JSONTariffPlansDataIN
from app.controllers import tariff_plan_service as service

security = Security(HTTPBearer())

tariff_plan_router = APIRouter(
    prefix='/tariff_plans',
    tags=['Tariff Plans'],
    responses={
        200: {'description': 'Success'},
        201: {'description': 'Created'},
        401: {'description': 'Unauthorized'},
        403: {'description': 'Forbidden'},
        400: {'description': 'Bad request'},
        404: {'description': 'Not found'},
    },
)


@tariff_plan_router.post('', response_model=TariffPlanData)
async def create_a_new_tariff_plan(data: TariffPlanDataIN, credentials: HTTPAuthorizationCredentials = security):
    if not service.is_valid_token(credentials.credentials):
        raise HTTPException(401, f'Failed to login.')
    result = await service.create_tariff_plan(date=data.date, rate=data.rate, cargo_type=data.cargo_type_name)
    return result


@tariff_plan_router.get('', response_model=List[TariffPlanData])
async def get_all_tariff_plans(credentials: HTTPAuthorizationCredentials = security):
    if not service.is_valid_token(credentials.credentials):
        raise HTTPException(401, f'Failed to login.')
    result = await service.get_all_tariff_plans()
    return result


@tariff_plan_router.put('/{tariff_plan_id}', response_model=TariffPlanData)
async def update_tariff_plan_by_id(tariff_plan_id: str, data: EditTariffPlanDataIN,
                                   credentials: HTTPAuthorizationCredentials = security):
    if not service.is_valid_token(credentials.credentials):
        raise HTTPException(401, f'Failed to login.')
    result = await service.update_tariff_plan(uuid.UUID(tariff_plan_id), cargo_type_id=data.cargo_type_id,
                                              rate=data.rate)
    return result


@tariff_plan_router.delete('/{tariff_plan_id}')
async def delete_tariff_plan_by_id(tariff_plan_id: str, credentials: HTTPAuthorizationCredentials = security):
    if not service.is_valid_token(credentials.credentials):
        raise HTTPException(401, f'Failed to login.')
    result = await service.delete_tariff_plane(tariff_plan_id)
    return result


@tariff_plan_router.post('/upload')
async def upload_tariff_plans_json(data: JSONTariffPlansDataIN, credentials: HTTPAuthorizationCredentials = security):
    if not service.is_valid_token(credentials.credentials):
        raise HTTPException(401, f'Failed to login.')
    return await service.upload_from_dict(data.data)
