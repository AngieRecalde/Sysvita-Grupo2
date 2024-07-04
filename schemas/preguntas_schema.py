from utils.ma import ma
from model.preguntas import Preguntas
from marshmallow import fields
from schemas.tests_schema import TestsSchema
class PreguntasSchema(ma.Schema):
    class Meta:
        model = Preguntas
        fields = ('id_pregunta','id_test','text_pregunta','orden')
    tests1 = ma.Nested(TestsSchema)    
pregunta_schema = PreguntasSchema()
preguntas_schema = PreguntasSchema(many=True)