from utils.ma import ma
from model.especialistas import Especialistas
from marshmallow import fields

class EspecialistasSchema(ma.Schema):
    class Meta:
        model = Especialistas
        fields = ('id_especialista','nombre','especialidad','email','telefono','fecha_registro','password')

especialista_schema = EspecialistasSchema()
especialistas_schema = EspecialistasSchema(many=True)
