from utils.ma import ma
from model.especialistas import Especialistas
from marshmallow import fields
from schemas.usuarios_schema import UsuarioSchema

class EspecialistasSchema(ma.Schema):
    class Meta:
        model = Especialistas
        fields = ('id_especialista',
                 'id_usuario',
                 'nombre',
                 'especialidad',
                 'fecha_registro',
                 'telefono')
        usuario2 = ma.Nested(UsuarioSchema)  

especialista_schema = EspecialistasSchema()
especialistas_schema = EspecialistasSchema(many=True)