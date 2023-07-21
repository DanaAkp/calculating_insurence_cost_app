from typing import List

from fastapi import APIRouter
from app.controllers import transfers_service as service
from app.routers.swagger_models import CargoTypeData, CalculatingDataIn, CalculatingData
transfers_router = APIRouter(
    prefix='/transfers',
    tags=['Transfers'],
    responses={
        200: {'description': 'Success'},
        201: {'description': 'Created'},
        401: {'description': 'Unauthorized'},
        403: {'description': 'Forbidden'},
        400: {'description': 'Bad request'},
        404: {'description': 'Not found'},
    },
)


@transfers_router.get('/cargo_types')
async def get_all_cargo_type() -> List:
    result = await service.get_all_cargo_type()
    return result


@transfers_router.post('/calculate')
async def calculating_insurance_cost_by_rate(data: CalculatingDataIn) -> CalculatingData:
    result = await service.calculating_insurance(data.declared_value, data.cargo_type_id)
    return result
