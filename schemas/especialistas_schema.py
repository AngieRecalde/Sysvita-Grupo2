from utils.ma import ma
from model.especialistas import Especialistas
from schemas.personas_schema import PersonasSchema
from marshmallow import fields

class EspecialistasSchema(ma.Schema):
    class Meta:
        model = Especialistas
        fields = ('id_especialista','id_persona','especialidad')
    persona1 = ma.Nested(PersonasSchema)
especilista_schema = EspecialistasSchema()
especilistas_schema = EspecialistasSchema(many=True)