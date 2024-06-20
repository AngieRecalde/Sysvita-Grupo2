from utils.ma import ma
from model.preguntas import Preguntas
from marshmallow import fields
from schemas.test_schema import TestSchema
class PreguntasSchema(ma.Schema):
    class Meta:
        model = Preguntas
        fields = ('id_pregunta','id_test','enunciado','tipo_escala','numero_pregunta')
    tests = ma.Nested(TestSchema)    
pregunta_schema = PreguntasSchema()
preguntas_schema = PreguntasSchema(many=True)