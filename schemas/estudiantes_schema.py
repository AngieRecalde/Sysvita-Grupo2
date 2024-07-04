from utils.ma import ma
from model.estudiantes import Estudiantes
from marshmallow import fields
from schemas.personas_schema import PersonasSchema
class EstudiantesSchema(ma.Schema):
    class Meta:
        model = Estudiantes
        fields = ('id_estudiante','id_persona','carrera')
    persona2 = ma.Nested(PersonasSchema)    
estudiante_schema = EstudiantesSchema()
estudiantes_schema = EstudiantesSchema(many=True)