from utils.ma import ma
from model.respuestas import Respuestas
from marshmallow import fields
from schemas.opciones_schema import OpcionesSchema
from schemas.test_schema import TestsSchema
from schemas.estudiantes_schema import EstudiantesSchema

class RespuestasSchema(ma.Schema):
    class Meta:
        model = Respuestas 
        fields = ('id_respuesta', 'id_test', 'id_opcion', 'id_estudiante')

    opcion = ma.Nested(OpcionesSchema)
    test = ma.Nested(TestsSchema)
    estudiante = ma.Nested(EstudiantesSchema)

respuesta_schema = RespuestasSchema()
respuestas_schema = RespuestasSchema(many=True)