from app.controllers.transfers import TransfersService
transfers_service = TransfersService()

from app.controllers.tariff_plan import TariffPlanService  # noqa fix circular import
tariff_plan_service = TariffPlanService()
