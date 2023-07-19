import datetime
from logging.config import dictConfig
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config import DB_URL, log_config
from app.routers.tariff_plan import tariff_plan_router
from app.routers.transfers import transfers_router
from app.controllers import tariff_plan_service
from app.models import TariffPlan


dictConfig(log_config)
app = FastAPI(title='CalculatingInsuranceApp')

app.include_router(transfers_router)
app.include_router(tariff_plan_router)

register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event('startup')
async def startup_event():
    if not await TariffPlan.all():
        await tariff_plan_service.create_tariff_plan(
            date=datetime.date(2001, 1, 1), cargo_type='other', rate=0.04
        )
