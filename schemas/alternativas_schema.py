from utils.ma import ma
from model.alternativas import Alternativas
from schemas.preguntas_schema import PreguntasSchema
from marshmallow import fields

class AlternativasSchema(ma.Schema):
    class Meta:
        model = Alternativas
        fields = ('id_alternativa','id_pregunta','texto_opcion','valor')
    pregunta = ma.Nested(PreguntasSchema)
alternativa_schema = AlternativasSchema()
alternativas_schema = AlternativasSchema(many=True)