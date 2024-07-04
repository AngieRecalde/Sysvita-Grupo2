from utils.ma import ma
from model.niveles import Niveles
from marshmallow import fields

class NivelesSchema(ma.Schema):
    model = Niveles
    id_nivel = fields.Integer()
    tipo_nivel = fields.String()
    nombre_nivel = fields.String()
    color = fields.String()


nivel_schema = NivelesSchema()
niveles_schema = NivelesSchema(many = True)