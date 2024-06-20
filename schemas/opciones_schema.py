from utils.ma import ma
from model.opciones import Opciones
from marshmallow import fields
from schemas.preguntas_schema import PreguntasSchema
class OpcionesSchema(ma.Schema):
    class Meta:
        model = Opciones
        fields = ('id_opcion','id_pregunta','texto_opcion','valor_opciona')
    pregunta = ma.Nested(PreguntasSchema)    
opcion_schema = OpcionesSchema()
opciones_schema = OpcionesSchema(many=True)