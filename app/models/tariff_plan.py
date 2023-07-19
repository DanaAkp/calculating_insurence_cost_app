from tortoise.models import Model
from tortoise import fields


class TariffPlan(Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(null=False)
    cargo_type = fields.ForeignKeyField(model_name='models.CargoType', related_name="tariff_plans")
    rate = fields.FloatField()

    class Meta:
        table = "tariff_plan"
        unique_together = (("date", "cargo_type_id"),)
