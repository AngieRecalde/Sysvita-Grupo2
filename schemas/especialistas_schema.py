from utils.ma import ma
from model.especialistas import Especialistas
from marshmallow import fields


class EspecialistasSchema(ma.Schema):
    class Meta:
        model = Especialistas
        field = ('id_especialista',
                 'nombre',
                 'especialidad',
                 'email',
                 'telefono',
                 'fecha_registro',
                 'password')

especilista_schema = EspecialistasSchema()
especilistas_schema = EspecialistasSchema(many=True)
