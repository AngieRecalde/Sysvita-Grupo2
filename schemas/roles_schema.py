from utils.ma import ma
from model.roles import Roles
from marshmallow import fields

class RolesSchema(ma.Schema):
    model = Roles
    id_rol = fields.Integer()
    nombre_rol= fields.String(max_length=50)


rol_schema = RolesSchema()
roles_schema = RolesSchema(many = True)