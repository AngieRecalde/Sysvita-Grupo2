from utils.ma import ma
from model.usuarios import Usuarios
from marshmallow import fields
from schemas.personas_schema import PersonasSchema
from schemas.roles_schema import RolesSchema
class UsuariosSchema(ma.Schema):
    class Meta:
        model = Usuarios
        fields = ('id_usuario',
                  'id_persona',
                  'id_rol',
                  'email',
                  'password_hash',
                  'fechaupdateuser')
    rol = ma.Nested(RolesSchema)
    persona3 = ma.Nested(PersonasSchema)    

usuario_schema = UsuariosSchema()
Usuarios_schema = UsuariosSchema(many=True)