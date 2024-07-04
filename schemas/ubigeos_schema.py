from utils.ma import ma
from model.ubigeos import Ubigeos
from marshmallow import fields

class UbigeosSchema(ma.Schema):
    model = Ubigeos
    id_ubigeo = fields.Integer()
    departamento = fields.String(max_length=50)
    provincia = fields.String(max_length=50)
    distrito = fields.String(max_length=50)
    poblacion = fields.String(max_length=50)
    superficie = fields.String(max_length=50)
    y = fields.Decimal(as_string=True)
    x = fields.Decimal(as_string=True)

ubigeo_schema = UbigeosSchema()
ubigeos_schema = UbigeosSchema(many = True)