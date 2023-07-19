from logging.config import dictConfig
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config import DB_URL, log_config
from app.routers.tariff_plan import tariff_plan_router
from app.routers.transfers import transfers_router


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
