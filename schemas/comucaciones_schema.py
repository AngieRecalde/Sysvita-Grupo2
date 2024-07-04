from utils.ma import ma
from model.comunicaciones import Comunicaciones
from schemas.evaluacionespecialista_schema import Evaluacion_EspecialistasSchema
from marshmallow import fields

class ComunicacionesSchema(ma.Schema):
    class Meta:
        model = Comunicaciones
        fields = ('id_comunicacion','id_evaluacion','recomendacion')
    comunicacion = ma.Nested(Evaluacion_EspecialistasSchema)
comunicacion_schema = ComunicacionesSchema()
comunicaciones_schema = ComunicacionesSchema(many=True)