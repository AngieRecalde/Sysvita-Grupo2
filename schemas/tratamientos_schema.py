from utils.ma import ma
from model.tratamientos import Tratamientos
from schemas.evaluacionespecialista_schema import Evaluacion_EspecialistasSchema
from marshmallow import fields

class TratamientosSchema(ma.Schema):
    class Meta:
        model = Tratamientos
        fields = ('id_tratamiento','id_evaluacion','descripcion')
    tratamiento= ma.Nested(Evaluacion_EspecialistasSchema)
tratamiento_schema = TratamientosSchema()
tratamientos_schema = TratamientosSchema(many=True)