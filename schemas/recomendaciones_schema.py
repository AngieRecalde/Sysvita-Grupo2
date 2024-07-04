from utils.ma import ma
from model.recomendaciones import Recomendaciones
from marshmallow import fields
from schemas.resultadostests_schema import ResultadosTestsSchema
from schemas.especialistas_schema import EspecialistasSchema
from schemas.estudiantes_schema import EstudiantesSchema

class RecomendacionesSchema(ma.Schema):
    class Meta:
        model = Recomendaciones
        fields = ('id_recomendacion',
                  'id_resultado',
                  'id_especialista',
                  'id_estudiante',
                  'fecha_envio',
                  'contenido')
    resultadotest = ma.Nested(ResultadosTestsSchema) 
    especialista3 = ma.Nested(EspecialistasSchema) 
    estudiante3 = ma.Nested(EstudiantesSchema) 
recomendacion_schema = RecomendacionesSchema()
recomendaciones_schema = RecomendacionesSchema(many=True)