from tortoise.models import Model
from tortoise import fields


class CargoType(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = "cargo_type"
